from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.data_manager import DataManager
from models.ml_models import MLModels
import pandas as pd
import os

router = APIRouter()
data_manager = DataManager()
ml_models = MLModels()

# Load predictions data if available
_predictions_df = None
def get_predictions_data():
    """Load predictions CSV if available and convert areas from hectares to km²"""
    global _predictions_df
    if _predictions_df is None:
        predictions_path = os.path.join(os.path.dirname(__file__), "..", "forest_predictions_2011_2075.csv")
        if os.path.exists(predictions_path):
            _predictions_df = pd.read_csv(predictions_path)
            
            # CRITICAL: Convert area from hectares to km² (same as main data)
            # FAO data reports areas in hectares (1 hectare = 0.01 km²)
            if 'area' in _predictions_df.columns:
                _predictions_df['area'] = _predictions_df['area'] / 100.0
        else:
            _predictions_df = pd.DataFrame()  # Empty DataFrame if file doesn't exist
    return _predictions_df

class PredictionRequest(BaseModel):
    forest_cover_2000: float
    total_area: float
    model_type: str = "random_forest"

@router.on_event("startup")
async def train_models_on_startup():
    """Train models when router is loaded"""
    try:
        df = data_manager.get_data()
        ml_models.train(df)
    except:
        pass  # Will be trained on first request if this fails

@router.get("/models/performance")
async def get_model_performance():
    """Get ML model performance metrics"""
    try:
        if not data_manager.is_initialized():
            data_manager.initialize()
        
        if not ml_models.is_trained():
            df = data_manager.get_data()
            ml_models.train(df)
        
        metrics = ml_models.get_metrics()
        return {"success": True, "data": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
async def predict_forest_cover(request: PredictionRequest):
    """Predict 2010 forest cover based on 2000 data"""
    try:
        if not data_manager.is_initialized():
            data_manager.initialize()
        
        if not ml_models.is_trained():
            df = data_manager.get_data()
            ml_models.train(df)
        
        prediction = ml_models.predict(
            request.forest_cover_2000,
            request.total_area,
            request.model_type
        )
        
        return {
            "success": True,
            "data": {
                "model_used": request.model_type,
                "input": {
                    "forest_cover_2000_percent": request.forest_cover_2000,
                    "total_area_km2": request.total_area
                },
                "predicted_forest_cover_2010_percent": prediction
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/time-series/{country_name}")
async def get_time_series_data(country_name: str, start_year: int = 2000, end_year: int = 2075):
    """Get forest cover time series data for a country (2000-2075)
    
    Data classification:
    - 2000-2010: Real data (from FAO Global Forest Resources Assessment)
    - 2011-2025: Interpolated/modeled data (based on trends and verified sources)
    - 2026-2075: Predictions (ML model forecasts)
    """
    try:
        if not data_manager.is_initialized():
            data_manager.initialize()
        
        time_series = data_manager.get_forest_cover_by_year(country_name, start_year, end_year)
        
        if time_series is None:
            raise HTTPException(
                status_code=404,
                detail=f"Country '{country_name}' not found or time series data not available"
            )
        
        return {
            "success": True,
            "data": time_series,
            "data_classification": {
                "real": "Actual measurements from FAO (2000-2010)",
                "interpolated": "Model-based/interpolated data verified against trends (2011-2025)",
                "prediction": "ML model forecasts (2026-2075)"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/future/{country_name}")
async def get_future_predictions(country_name: str, start_year: int = 2026, end_year: int = 2075):
    """Get future forest cover predictions for a country (2026-2075)
    
    Note: For historical data (2000-2025), use /time-series endpoint
    """
    try:
        if not data_manager.is_initialized():
            data_manager.initialize()
        
        if start_year < 2026:
            raise HTTPException(
                status_code=400,
                detail="For data before 2026, use /time-series endpoint. This endpoint is for predictions (2026-2075)"
            )
        
        time_series = data_manager.get_forest_cover_by_year(country_name, start_year, end_year)
        
        if time_series is None:
            raise HTTPException(
                status_code=404,
                detail=f"Country '{country_name}' not found or predictions data not available"
            )
        
        # Filter only predictions (2026+)
        predictions_data = {
            year: data
            for year, data in time_series["data"].items()
            if data["data_type"] == "prediction"
        }
        
        return {
            "success": True,
            "data": {
                "country": time_series["country"],
                "area_km2": time_series["area_km2"],
                "predictions": predictions_data
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country/{country_name}/year/{year}")
async def get_country_year_data(country_name: str, year: int):
    """Get forest cover data for a specific country and year (2000-2075)
    
    Args:
        country_name: Name of the country (case-insensitive)
        year: Year between 2000 and 2075
    
    Returns:
        Forest cover percentage, data type, and country information
    """
    try:
        if not data_manager.is_initialized():
            data_manager.initialize()
        
        # Validate year range
        if year < 2000 or year > 2075:
            raise HTTPException(
                status_code=400,
                detail=f"Year must be between 2000 and 2075. Received: {year}"
            )
        
        # Get time series data for the specific year
        time_series = data_manager.get_forest_cover_by_year(country_name, year, year)
        
        if time_series is None:
            raise HTTPException(
                status_code=404,
                detail=f"Country '{country_name}' not found"
            )
        
        year_str = str(year)
        if year_str not in time_series["data"]:
            raise HTTPException(
                status_code=404,
                detail=f"Data for year {year} not available for country '{country_name}'"
            )
        
        year_data = time_series["data"][year_str]
        
        # Calculate forest area in km²
        forest_area_km2 = (time_series["area_km2"] * year_data["forest_cover_percent"]) / 100.0
        
        return {
            "success": True,
            "data": {
                "country": time_series["country"],
                "year": year,
                "area_km2": float(time_series["area_km2"]),
                "forest_cover_percent": year_data["forest_cover_percent"],
                "forest_area_km2": float(forest_area_km2),
                "data_type": year_data["data_type"],
                "data_type_description": {
                    "real": "Actual measurements from FAO (2000-2010)",
                    "interpolated": "Model-based/interpolated data verified against trends (2011-2025)",
                    "prediction": "ML model forecasts (2026-2075)"
                }.get(year_data["data_type"], "Unknown")
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
