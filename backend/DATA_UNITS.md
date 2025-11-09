# Data Units Documentation

## Area Units

### Source Data Format
The CSV files (`Deforestation.csv` and `forest_predictions_2011_2075.csv`) contain area measurements in **hectares**.

**Source**: FAO (Food and Agriculture Organization) Global Forest Resources Assessment data typically reports areas in hectares.

### Conversion
All area columns are automatically converted from **hectares to km²** when data is loaded.

**Conversion Formula**: `km² = hectares / 100`

### Verified Country Areas
After conversion, areas match known country areas (within 1-2%):
- **Afghanistan**: 643,857 km² (known: 652,230 km²) - 1.28% difference ✓
- **Canada**: 9,834,230 km² (known: 9,984,670 km²) - 1.51% difference ✓
- **Brazil**: 8,500,356 km² (known: 8,514,877 km²) - 0.17% difference ✓

### Area Columns in API Responses
All area values in API responses are in **km²**:
- `total_area_km2`
- `forest_cover_2000_km2`
- `forest_cover_2010_km2`
- `change_km2`
- `forest_loss_km2`
- `forest_gain_km2`

## Delta Convention

### Delta Percent
- **Formula**: `delta_percent = forest_cover_2000 - forest_cover_2010`
- **Positive delta** = **Deforestation** (loss)
- **Negative delta** = **Reforestation** (gain)
- **Zero delta** = No change

### Delta Area
- **Formula**: `delta_area = forest_area_2000 - forest_area_2010`
- **Units**: km² (after conversion from hectares)
- **Positive delta** = **Forest loss** (deforestation)
- **Negative delta** = **Forest gain** (reforestation)

## Data Source
- **Main Data**: `Deforestation.csv` - 235 countries, 2000-2010 data
- **Predictions**: `forest_predictions_2011_2075.csv` - 235 countries, 2011-2075 predictions
- **Source**: FAO Global Forest Resources Assessment / Achebe_ml_model branch

## Implementation
The conversion happens automatically in `models/data_manager.py` in the `_load_and_clean_data()` method:
```python
# Convert hectares to km² (divide by 100)
df_clean[col] = df_clean[col] / 100.0
```

All calculations and API responses use km² consistently.

