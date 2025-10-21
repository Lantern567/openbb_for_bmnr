# OpenBB Workspace Backend for BMNR Analysis

This FastAPI backend provides custom widgets for BMNR stock analysis in OpenBB Workspace.

## Features

- **Technical Analysis Chart**: Interactive candlestick charts with moving averages
- **mNAV Analysis**: Modified Net Asset Value calculation and visualization
- **Price Data Table**: Historical OHLCV data
- **Key Metrics**: Real-time metrics dashboard
- **Scenario Analysis**: Compare multiple mNAV valuation scenarios

## Installation

### Prerequisites

1. Install main project dependencies first:
```bash
cd ..
pip install -r requirements.txt
```

2. Install backend-specific dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Running the Backend

### Method 1: Using uvicorn directly

```bash
cd backend
uvicorn main:app --port 8000 --reload
```

### Method 2: Using Python

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

### Verify it's running

Open your browser and go to:
- API docs: `http://localhost:8000/docs`
- Root endpoint: `http://localhost:8000/`

## Connecting to OpenBB Workspace

### Step 1: Start the Backend

Make sure the backend is running on `localhost:8000`

### Step 2: Open OpenBB Workspace

Go to [https://pro.openbb.co](https://pro.openbb.co) and log in

### Step 3: Connect Backend

1. Click on the **"Apps"** tab in the left sidebar
2. Click **"Connect backend"** button
3. Fill in the form:
   - **Name**: `BMNR Analysis`
   - **URL**: `http://localhost:8000`
4. Click **"Test"** to verify the connection
   - You should see: "Test successful - Found 5 widgets"
5. Click **"Add"** to add the backend

### Step 4: Use Widgets

1. Go to the **"Dashboard"** tab
2. Click **"Add Widget"**
3. Find your widgets under "BMNR Analysis Backend" or search for "BMNR"
4. Available widgets:
   - BMNR Technical Analysis
   - BMNR mNAV Analysis
   - BMNR Price Data
   - BMNR Key Metrics
   - BMNR mNAV Scenarios

### Step 5: Configure Widgets

Each widget has parameters you can adjust:

**Technical Analysis:**
- Symbol (default: BMNR)
- Days of History (default: 365)

**mNAV Analysis:**
- Symbol
- Days of History
- Shares Outstanding (important!)
- Property Fair Value (optional)
- Property Book Value (optional)
- Deferred Tax Rate

**Metrics:**
- Symbol
- Shares Outstanding

## API Endpoints

### Configuration Endpoints

- `GET /` - API information
- `GET /widgets.json` - Widget configuration
- `GET /apps.json` - Apps configuration

### Data Endpoints

- `GET /bmnr/technical_chart` - Technical analysis chart
- `GET /bmnr/mnav_chart` - mNAV analysis chart
- `GET /bmnr/price_table` - Historical price data table
- `GET /bmnr/metrics` - Key metrics
- `GET /bmnr/scenario_analysis` - mNAV scenario comparison

### Query Parameters

Most endpoints accept:
- `symbol` - Stock ticker (default: "BMNR")
- `days` - Number of days of historical data
- `theme` - Chart theme ("dark" or "light")
- `raw` - Return raw data for AI analysis (boolean)

mNAV endpoints also accept:
- `shares_outstanding` - Total shares outstanding
- `property_fair_value` - Fair value of properties
- `property_book_value` - Book value of properties
- `deferred_tax_rate` - Tax rate for adjustments

## Theme Support

The backend automatically adapts to OpenBB Workspace's theme:
- Dark mode: Uses dark color scheme
- Light mode: Uses light color scheme

The `theme` parameter is automatically passed by OpenBB Workspace.

## Troubleshooting

### Connection Failed

**Issue**: OpenBB Workspace can't connect to `http://localhost:8000`

**Solutions**:
1. Verify backend is running: Check terminal for "Uvicorn running on..."
2. Check the URL: Must be `http://localhost:8000` (not `127.0.0.1`)
3. Check firewall: Allow connections on port 8000
4. Try restarting the backend

### No Data or Errors

**Issue**: Widgets show errors or no data

**Solutions**:
1. Check BMNR is the correct symbol
2. Verify internet connection (for data fetching)
3. Check backend logs in terminal for errors
4. Verify `shares_outstanding` is set correctly for mNAV

### Widgets Not Showing

**Issue**: Can't find widgets in OpenBB Workspace

**Solutions**:
1. Click "Test" in backend connection to verify
2. Refresh OpenBB Workspace page
3. Check `/widgets.json` endpoint in browser
4. Verify CORS is properly configured

### Theme Not Applying

**Issue**: Charts don't match OpenBB theme

**Solution**: The `theme` parameter is automatically handled by OpenBB. If issues persist, check browser console for errors.

## Development

### Adding New Widgets

1. Add endpoint in `main.py`
2. Add widget definition in `widgets.json`
3. Test locally
4. Refresh connection in OpenBB Workspace

### Modifying Existing Widgets

1. Edit endpoint in `main.py`
2. Update parameters in `widgets.json` if needed
3. Restart backend
4. Refresh widgets in OpenBB Workspace

## Security Notes

- This backend runs on **localhost only** by default
- Only you can access it
- Data is not uploaded to OpenBB servers
- To deploy publicly, use proper authentication

## Cloud Deployment (Optional)

To access from anywhere:

1. Deploy to Heroku/Railway/DigitalOcean
2. Get public URL (e.g., `https://your-app.herokuapp.com`)
3. Update CORS in `main.py` if needed
4. Connect using public URL in OpenBB Workspace

## License

Same as main project.

## Support

For issues:
1. Check this README
2. Check main project README
3. Review OpenBB Workspace docs: https://docs.openbb.co/workspace
4. Check FastAPI docs: https://fastapi.tiangolo.com

---

**Built for OpenBB Workspace** 🚀
