# Analytics Platform

An end-to-end analytics platform built with Python, PostgreSQL, and .NET Web API.

## Architecture Overview    

CSV / JSON Input Files
        ↓
Python Pipeline (Ingest → Validate → Anomaly Detect → AI Insights)
        ↓
PostgreSQL (6 Tables)
        ↓
.NET 10 Web API (8 Endpoints)
        ↓
REST Responses + Visualizations

## Tech Stack

Tech Stack		
        
Tech Stack		
        
Layer	Technology	Purpose
Data Ingestion	Python + Pandas	Reads CSV and JSON input files
Validation	Python	Field-level and type-level checks
Anomaly Detection	Python + SciPy	Z-Score and IQR methods combined
AI Insights	OpenAI / Mock	Human-readable business insights
Database	PostgreSQL 15	Stores all processed data
Web API	.NET 10	Exposes 8 REST endpoints
Visualizations	Matplotlib + Seaborn	5 charts saved as PNG
CI Pipeline	GitHub Actions	Auto-checks on every push
Orchestration	Docker Compose	One command local setup



## Project Structure

analytics-platform/
├── docker-compose.yml                  # Runs all 3 services
├── README.md                           # This file
├── DESIGN_DECISIONS.md                 # Tradeoffs and improvements
├── PROJECT_OVERVIEW.md                 # Project summary
├── postman_collection.json             # API testing collection
│
├── .github/
│   └── workflows/
│       └── ci.yml                      # GitHub Actions CI pipeline
│
├── python-pipeline/
│   ├── Dockerfile                      # Python container definition
│   ├── requirements.txt                # Python dependencies
│   ├── main.py                         # Pipeline entry point
│   ├── db.py                           # Database connection
│   ├── ingestion/
│   │   └── ingestor.py                 # CSV + JSON ingestion
│   ├── validation/
│   │   └── validator.py                # Record validation logic
│   ├── anomaly/
│   │   └── detector.py                 # Z-Score + IQR detection
│   └── insights/
│       └── ai_insights.py              # OpenAI + mock fallback
│
├── dotnet-api/
│   └── AnalyticsPlatform/
│       ├── Dockerfile                  # .NET container definition
│       ├── Program.cs                  # App startup + Serilog
│       ├── Controllers/
│       │   └── AnalyticsController.cs  # All 8 API endpoints
│       ├── Models/
│       │   └── AnalyticsModels.cs      # C# model classes
│       └── Data/
│           └── AnalyticsDbContext.cs   # EF Core DB context
│
├── sql/
│   ├── 01_schema.sql                   # Creates all 6 tables
│   └── 02_analytics.sql                # 7 analytical queries
│
├── notebooks/
│   └── analytics_visualization.py      # 5 chart visualizations
│
└── data/
    ├── sales_data.csv                  # 25 sample records (CSV)
    ├── sales_data.json                 # 10 sample records (JSON)
    └── sample_outputs.json             # Sample API responses

1. Clone the Repository
git clone https://github.com/vimalancodes/Analytics-Platform.git
cd Analytics-Platform

2. Start All Services

docker-compose up --build

This single command will:
Build Python pipeline and .NET API Docker images
Start PostgreSQL with correct credentials
Wait for PostgreSQL to be healthy
Run the Python pipeline — ingests, validates, detects anomalies, generates insights
Start the .NET API on port 5000

3. Verify Everything is Running
You should see these logs:

4. Test the API
Open your browser or Postman and hit:
http://localhost:5000/api/analytics/summary
http://localhost:5000/api/analytics/anomalies

5. Stop Everything
docker-compose down

Manual Run (Without Full Docker)
If you prefer to run services manually:

## Quick Start

### 1. Start PostgreSQL
```bash
docker-compose up -d postgres
```

### 2. Create Schema
```bash
docker exec -i analytics_db psql -U analytics_user -d analytics_db -f /docker-entrypoint-initdb.d/01_schema.sql
```

### 3. Run Python Pipeline
```bash
cd python-pipeline
pip install -r requirements.txt
python main.py
```

### 4. Run .NET API
```bash
cd dotnet-api/AnalyticsPlatform
dotnet run
```

### 5. Run Visualizations
```bash
cd notebooks
python analytics_visualization.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/analytics/summary | Summary metrics |
| GET | /api/analytics/anomalies | Detected anomalies |
| GET | /api/analytics/invalid-records | Failed validation records |
| GET | /api/analytics/insights | AI generated insights |
| GET | /api/analytics/valid-records | All valid records |
| GET | /api/analytics/revenue-by-region | Revenue grouped by region |
| GET | /api/analytics/revenue-by-category | Revenue grouped by category |
| POST | /api/analytics/process | Trigger pipeline info |

## Sample Data

- **sales_data.csv** — 25 records with intentional invalid entries
- **sales_data.json** — 10 records with intentional anomalies

## Anomaly Detection

Two methods used:
- **Z-Score** — flags records with score > 2.5
- **IQR** — flags records outside 1.5x interquartile range

## AI Insights Layer

- Uses **OpenAI GPT-3.5** if API key is provided
- Falls back to **mock insights** if no key available
- Set `OPENAI_API_KEY` environment variable to enable real AI




