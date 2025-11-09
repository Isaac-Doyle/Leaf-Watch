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

@router.get("/future/{country_name}")
async def get_future_predictions(country_name: str, start_year: int = 2011, end_year: int = 2075):
    """Get future forest cover predictions for a country (2011-2075)"""
    try:
        if not data_manager.is_initialized():
            data_manager.initialize()
        
        predictions_df = get_predictions_data()
        if predictions_df.empty:
            raise HTTPException(
                status_code=404,
                detail="Predictions data not available"
            )
        
        # Find country (case-insensitive)
        country_data = predictions_df[
            predictions_df['country'].str.lower() == country_name.lower()
        ]
        
        if country_data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"Country '{country_name}' not found in predictions data"
            )
        
        country_row = country_data.iloc[0]
        
        # Get year columns (2011-2075)
        year_columns = [str(year) for year in range(start_year, end_year + 1) if str(year) in predictions_df.columns]
        
        if not year_columns:
            raise HTTPException(
                status_code=400,
                detail=f"No prediction data available for years {start_year}-{end_year}"
            )
        
        # Extract predictions
        predictions = {
            "country": country_row['country'],
            "area_km2": float(country_row['area']),
            "baseline_2000": float(country_row.get('2000', 0)),
            "baseline_2010": float(country_row.get('2010', 0)),
            "predictions": {
                year: float(country_row[year]) for year in year_columns
            }
        }
        
        return {
            "success": True,
            "data": predictions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
