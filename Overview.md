COMMAND                          WHAT HAPPENS
─────────────────────────────────────────────────────
docker-compose up --build   →   starts all 3 services

                                 PostgreSQL ✅
                                     ↓
                                 Python Pipeline
                                   reads CSV + JSON (35 records)
                                   validates → 28 valid, 7 invalid
                                   detects → 4 anomalies
                                   generates AI insights
                                   stores everything in PostgreSQL ✅
                                     ↓
                                 .NET API starts
                                   listening on port 5000 ✅

─────────────────────────────────────────────────────
TEST ENDPOINTS:
http://localhost:5000/api/analytics/summary
http://localhost:5000/api/analytics/anomalies
http://localhost:5000/api/analytics/invalid-records
http://localhost:5000/api/analytics/insights
http://localhost:5000/api/analytics/revenue-by-region
http://localhost:5000/api/analytics/revenue-by-category

─────────────────────────────────────────────────────
OPTIONAL — Run visualizations manually:
cd notebooks
python analytics_visualization.py
→ generates 5 PNG charts