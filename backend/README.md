# Backend API - FastAPI Employee Attrition Prediction

FastAPI-based REST API for employee attrition prediction, employee record management, and model serving.

## Project Structure

```
backend/
├── venv/                      # Python virtual environment
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── app/
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Configuration management
│   ├── database.py           # Database connection and session
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic request/response schemas
│   └── routes/
│       ├── predictions.py     # Prediction endpoints
│       ├── employees.py       # Employee management endpoints
│       └── health.py          # Health check endpoint
├── tests/
│   ├── test_predictions.py   # Prediction endpoint tests
│   ├── test_employees.py     # Employee endpoint tests
│   └── http/
│       └── api.http           # REST Client requests
└── migrations/                # Alembic database migrations
    ├── env.py
    ├── script.py.mako
    └── versions/
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
./venv/Scripts/activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env`:

```
DATABASE_URL=sqlite:///./attrition.db
API_BASE_URL=http://localhost:8000
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
ENVIRONMENT=development
```

### 4. Initialize Database

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 5. Run the Server

```bash
python -m uvicorn app.main:app --reload
```

Server will start at `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

## API Endpoints

### Health Check

```
GET /api/health
```

Response:

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Single Prediction

```
POST /api/predict
```

Request body (Pydantic model):

```json
{
  "age": 45,
  "monthly_income": 5000,
  "years_at_company": 10,
  "job_satisfaction": 3,
  "department": "Sales",
  "job_role": "Sales Executive"
}
```

Response:

```json
{
  "attrition_risk": true,
  "probability": 0.72,
  "risk_level": "High",
  "confidence": 0.85
}
```

### Batch Prediction (CSV Upload)

```
POST /api/predict/batch
```

Request:

- `file`: CSV file with employee records (multipart/form-data)

Response:

```json
{
  "processed_count": 100,
  "results_file": "results_batch_20240110_120000.csv",
  "download_url": "/api/predict/batch/download/results_batch_20240110_120000.csv"
}
```

### Employee Records

```
GET /api/employees
```

Query parameters:

- `skip`: Pagination offset (default: 0)
- `limit`: Records per page (default: 50)
- `department`: Filter by department

Response:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "department": "Sales",
    "age": 45,
    "monthly_income": 5000,
    "years_at_company": 10,
    "attrition_risk": true,
    "probability": 0.72,
    "created_at": "2024-01-10T12:00:00"
  }
]
```

```
POST /api/employees
```

Request body:

```json
{
  "name": "Jane Smith",
  "department": "IT",
  "age": 35,
  "monthly_income": 6500,
  "years_at_company": 5
}
```

### Model Metrics

```
GET /api/model/metrics
```

Response:

```json
{
  "model_version": "1.0.0",
  "training_date": "2024-01-08",
  "accuracy": 0.87,
  "precision": 0.84,
  "recall": 0.82,
  "f1_score": 0.83,
  "roc_auc": 0.92,
  "confusion_matrix": [
    [1200, 50],
    [100, 120]
  ]
}
```

## Database Schema

### employees table

```sql
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  department VARCHAR(100),
  age INTEGER,
  monthly_income DECIMAL(10, 2),
  years_at_company INTEGER,
  job_role VARCHAR(100),
  job_satisfaction INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### predictions table

```sql
CREATE TABLE predictions (
  id SERIAL PRIMARY KEY,
  employee_id INTEGER FOREIGN KEY REFERENCES employees(id),
  attrition_risk BOOLEAN,
  probability DECIMAL(5, 4),
  risk_level VARCHAR(20),
  confidence DECIMAL(5, 4),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### model_metrics table

```sql
CREATE TABLE model_metrics (
  id SERIAL PRIMARY KEY,
  model_version VARCHAR(50),
  training_date DATE,
  accuracy DECIMAL(5, 4),
  precision DECIMAL(5, 4),
  recall DECIMAL(5, 4),
  f1_score DECIMAL(5, 4),
  roc_auc DECIMAL(5, 4),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

Run all tests:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/test_predictions.py -v
```

Test coverage:

```bash
pytest --cov=app tests/
```

## Testing with REST Client

Install the REST Client extension (esbenp.rest-client) in VS Code.

Open `tests/http/api.http` and click "Send Request" on any endpoint to test manually.

## Configuration

Edit `app/config.py` for:

- Database URL
- CORS origins
- API settings
- Logging configuration

## Database Migrations

Create migration after model changes:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback last migration:

```bash
alembic downgrade -1
```

## Error Handling

API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad request (invalid input)
- **404**: Not found
- **422**: Validation error (Pydantic)
- **500**: Server error

Error response format:

```json
{
  "detail": "Error message"
}
```

## CORS Configuration

Backend is configured to accept requests from frontend origins specified in `.env`:

```
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

Update as needed for different deployment environments.

## Performance Optimization

- Database queries use connection pooling
- Model is loaded once at startup (cached)
- Batch predictions use bulk insert
- API includes caching headers where appropriate

## Logging

Configure logging level in `.env`:

```
LOG_LEVEL=INFO
```

Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

Logs output to console and optionally to files.

## Deployment

See `DEPLOY.md` in the root for production deployment instructions.

For Render deployment:

- Use PostgreSQL database
- Set `ENVIRONMENT=production`
- Use Gunicorn with Uvicorn workers
- Configure appropriate CORS origins
