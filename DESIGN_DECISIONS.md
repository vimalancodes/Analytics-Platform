# Design Decisions, Tradeoffs & Improvements

## Architecture Decisions

### 1. Python for Pipeline, .NET for API
Python was chosen for the pipeline because of its rich data ecosystem
(pandas, scipy, sqlalchemy). .NET was chosen for the API layer because
of its strong typing, performance, and enterprise readiness.

### 2. Raw Records Stored as TEXT
All raw ingested data is stored as TEXT in the raw_records table.
This prevents pipeline failures when dirty data arrives (e.g. "abc"
in a numeric field). Validation happens after ingestion, not before.

### 3. Two Anomaly Detection Methods
Both Z-Score and IQR methods are used together. Z-Score works well
for normally distributed data. IQR is more robust for skewed data.
Using both reduces false negatives.

### 4. AI Insights Service Abstraction
The AI insights layer uses a clean abstraction with two modes:
- Real mode: OpenAI GPT-3.5 via API key
- Mock mode: Rule-based insights when no API key is available
This makes the system testable without an API key and easy to swap
OpenAI for Azure OpenAI by just changing the client configuration.

### 5. Separation of Concerns
- Python owns data processing
- PostgreSQL owns storage and analytics
- .NET owns API and presentation
- Each layer is independently deployable

### 6. Docker Compose for Local Orchestration
Docker Compose ensures PostgreSQL runs consistently across all
environments without manual installation. Each service is isolated
in its own container with environment variables for configuration.

## Tradeoffs

| Decision | Benefit | Tradeoff |
|----------|---------|----------|
| TEXT for raw storage | No pipeline crashes on dirty data | Requires casting in queries |
| Mock AI fallback | Works without API key | Less intelligent insights |
| Separate Python + .NET | Best tool for each job | More complexity to deploy |
| Z-Score + IQR both | Better anomaly coverage | May produce duplicates |
| Read-only .NET API | Simple and safe | Cannot trigger pipeline via API |

## What I Would Improve With More Time

### Short Term
- Add unit tests for Python pipeline (pytest)
- Add integration tests for .NET API (xUnit)
- Add pagination to all API list endpoints
- Add API authentication (JWT tokens)
- Add input validation to API endpoints

### Medium Term
- Add GraphQL support via Hot Chocolate (.NET)
- Add real-time pipeline trigger from API endpoint
- Add Azure Blob Storage support for input files
- Add Azure OpenAI as alternative to OpenAI
- Add Prometheus metrics endpoint for monitoring

### Long Term
- Replace batch pipeline with streaming (Apache Kafka)
- Add ML-based anomaly detection (Isolation Forest)
- Add data lineage tracking
- Add multi-tenant support
- Deploy to Azure AKS with Helm charts

## Azure/OpenAI-Ready Design

The solution is designed to be Azure-ready:
- OpenAI key is environment variable — swap for Azure OpenAI endpoint easily
- PostgreSQL can be replaced with Azure Database for PostgreSQL
- Docker Compose can be converted to Azure Container Apps
- Serilog can be configured to write to Azure Application Insights
- Input files can be read from Azure Blob Storage with minimal changes