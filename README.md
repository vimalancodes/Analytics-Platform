# Analytics Platform

An end-to-end analytics platform built with Python, PostgreSQL, and .NET Web API.

## Architecture Overview    

CSV/JSON Data → Python Pipeline → PostgreSQL → .NET Web API → REST Endpoints
↓
Anomaly Detection
↓
AI Insights Layer
↓
Jupyter Visualization

## Tech Stack

- **Python 3.11** — Data ingestion, validation, anomaly detection, AI insights
- **PostgreSQL 15** — Data storage and analytical queries
- **.NET 10** — Web API layer
- **Docker Compose** — Local orchestration

## Project Structure

analytics-platform/
├── docker-compose.yml
├── python-pipeline/
│   ├── main.py               # Pipeline entry point
│   ├── db.py                 # Database connection
│   ├── ingestion/            # CSV + JSON ingestion
│   ├── validation/           # Pydantic-style validation
│   ├── anomaly/              # Z-Score + IQR detection
│   └── insights/             # OpenAI + mock AI insights
├── dotnet-api/
│   └── AnalyticsPlatform/    # .NET Web API
├── notebooks/
│   └── analytics_visualization.py
├── sql/
│   ├── 01_schema.sql         # Table definitions
│   └── 02_analytics.sql      # Analytical queries
└── data/
├── sales_data.csv        # Sample CSV input
└── sales_data.json       # Sample JSON input

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

## Design Decisions

- Raw records stored as TEXT to handle dirty data without pipeline failure
- Validation and anomaly detection are separate modules for maintainability
- AI insights use service abstraction — easy to swap OpenAI for Azure OpenAI
- .NET API is read-only — pipeline runs via Python for clear separation of concerns

## What I Would Improve With More Time

- Add GraphQL support via Hot Chocolate
- Add GitHub Actions CI pipeline
- Add pagination to API endpoints
- Add authentication to API
- Add real-time pipeline trigger from API
- Add Azure Blob Storage support for input files
- Add unit tests for Python pipeline and .NET API


