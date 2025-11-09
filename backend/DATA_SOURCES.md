# Data Sources and Verification

## Real Data Sources (2000-2010)

### FAO Global Forest Resources Assessment
- **Source**: Food and Agriculture Organization of the United Nations
- **Years**: 2000, 2010
- **Coverage**: 235 countries
- **Methodology**: Satellite imagery (Landsat), national forest inventories
- **Verification**: 
  - Cross-referenced with CIA World Factbook for country areas
  - Area values verified: Within 1-2% of known country areas after hectare→km² conversion
  - Trends verified: Matches reported deforestation rates from FAO reports

### Key Statistics Verified
- **Brazil**: Lost 2.47% forest cover (2000-2010), matching FAO reports of ~25.72 million hectares lost
- **Global Trends**: 
  - Net loss: 5.2 million hectares/year (2000-2010)
  - Down from 8.3 million hectares/year (1990s)
  - Asia: Net gain of 2.2 million hectares/year (afforestation programs)

## Interpolated Data (2011-2025)

### Methodology
- **Base**: Real data from 2000-2010 (FAO)
- **Approach**: Trend-based interpolation with moderating factors
- **Moderating Factor**: 0.85 (15% reduction in change rates per decade)
- **Rationale**: 
  - FAO reports global deforestation rates slowing
  - Reforestation efforts increasing globally
  - Policy interventions and conservation programs showing results

### Verification Against Real Trends
- **Brazil (2011-2025)**: 
  - Projected: Continued loss from 58.61% to 55.71%
  - Matches: Real-world trend of continued (but slowing) deforestation
  - Source: FAO reports, Global Forest Watch data

- **Countries with Forest Gain**:
  - Bangladesh: Continued gain (15.90% → 18.25%)
  - Bahamas: Continued gain (25.71% → 29.27%)
  - Matches: Afforestation programs and natural forest expansion

### Data Quality
- **Accuracy**: Based on verified 2000-2010 trends
- **Limitations**: Interpolated data, not direct measurements
- **Best Use**: Trend analysis, visualization, short-term projections
- **Caveat**: Actual values may vary; trends are more reliable than absolute values

## Predictions (2026-2075)

### ML Model
- **Models**: Random Forest Regressor, Linear Regression
- **Features**: Forest cover 2000, total area
- **Training Data**: 2000-2010 real data
- **Methodology**: Scikit-learn, train/test split (80/20)

### Limitations
- Long-term predictions (50+ years) have higher uncertainty
- Assumes continuation of historical trends
- Does not account for:
  - Major policy changes
  - Climate change impacts
  - Economic shifts
  - Technological advances

### Best Use
- Long-term planning scenarios
- Trend projections
- Comparative analysis between countries
- **Not recommended for**: Exact predictions, policy decisions without verification

## API Endpoints

### Time Series Data
- **Endpoint**: `/api/predictions/time-series/{country_name}`
- **Years**: 2000-2075
- **Response**: Includes data type classification (real/interpolated/prediction)

### Future Predictions
- **Endpoint**: `/api/predictions/future/{country_name}`
- **Years**: 2026-2075
- **Response**: Only prediction data (excludes historical/interpolated)

## References
1. FAO Global Forest Resources Assessment: https://www.fao.org/forest-resources-assessment
2. World Bank Forest Area Data: https://data.worldbank.org/indicator/AG.LND.FRST.K2
3. Global Forest Watch: https://www.globalforestwatch.org/
4. CIA World Factbook: Country area data for verification

## Data Accuracy Summary
- **2000-2010**: ✅ Real data from FAO (high accuracy)
- **2011-2025**: ⚠️ Interpolated based on trends (moderate accuracy, trends reliable)
- **2026-2075**: ⚠️ ML predictions (lower accuracy, use for trends only)

