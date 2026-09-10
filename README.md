# Employee Attrition Prediction

A full-stack web application for predicting employee attrition using machine learning. Built with FastAPI, React, and PostgreSQL.

## Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React/Vite)                │
│         - Prediction Form & Results Dashboard           │
│         - Employee Records Table                        │
│         - Bulk CSV Upload                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               Backend API (FastAPI)                      │
│         - /api/predict - Single prediction              │
│         - /api/predict/batch - Batch predictions        │
│         - /api/employees - Record management            │
│         - /api/model/metrics - Model performance        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌──────────┐
    │  ML    │  │ Database │  │ ML Model │
    │ Module │  │(Postgres)│  │  (PKL)   │
    └────────┘  └────────┘  └──────────┘
```

## Project Structure

```
.
├── ml/                          # ML model development
│   ├── venv/                    # Python virtual environment
│   ├── requirements.txt
│   ├── README.md
│   ├── data/
│   │   └── attrition.csv
│   ├── notebooks/
│   │   └── eda.ipynb
│   ├── src/
│   │   ├── preprocessing.py
│   │   ├── train.py
│   │   └── evaluate.py
│   └── models/
│       ├── model.pkl
│       ├── preprocessor.pkl
│       └── metrics.json
├── backend/                     # FastAPI backend
│   ├── venv/                    # Python virtual environment
│   ├── requirements.txt
│   ├── README.md
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   └── routes/
│   │       ├── predictions.py
│   │       ├── employees.py
│   │       └── health.py
│   ├── tests/
│   │   ├── test_predictions.py
│   │   ├── test_employees.py
│   │   └── http/
│   │       └── api.http
│   └── migrations/              # Alembic migrations
├── frontend/                    # React frontend
│   ├── node_modules/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── public/
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── pages/
│       ├── components/
│       ├── services/
│       └── styles/
├── .vscode/
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
├── .gitignore
├── README.md                    # This file
├── PROGRESS.md                  # Build progress log
└── DEPLOY.md                    # Deployment guide
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ (or use SQLite for local dev)
- Git

### Local Development Setup

1. **Clone and navigate to the project:**

   ```bash
   cd /path/to/Employee\ attrition\ prediction
   ```

2. **Install Python dependencies:**
   - ML module: `cd ml && python -m venv venv && ./venv/Scripts/pip install -r requirements.txt`
   - Backend: `cd ../backend && python -m venv venv && ./venv/Scripts/pip install -r requirements.txt`

3. **Install Node dependencies:**

   ```bash
   cd frontend && npm install
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` in the backend directory
   - Update database connection string and API base URL

5. **Run migrations:**

   ```bash
   cd backend && alembic upgrade head
   ```

6. **Start the services:**
   - Backend: `cd backend && .venv/Scripts/python -m uvicorn app.main:app --reload`
   - Frontend: `cd frontend && npm run dev`

### VS Code Tasks

Use the integrated terminal or the Task Runner (Ctrl+Shift+B):

- **Install ML Dependencies**: Sets up the ML Python environment
- **Install Backend Dependencies**: Sets up the backend Python environment
- **Install Frontend Dependencies**: Installs npm packages
- **Run Backend**: Starts the FastAPI development server
- **Run Frontend**: Starts the React dev server
- **Run Tests**: Executes backend test suite

### VS Code Debug Configurations

- **FastAPI Backend**: Debug the backend with breakpoints (F5)
- **Python: ML Script**: Debug individual ML scripts

## Features

- **Employee Prediction**: Single employee attrition risk prediction with confidence score
- **Batch Processing**: Upload CSV files for bulk predictions
- **Employee Database**: Store and manage employee records with prediction history
- **Performance Dashboard**: Visualize attrition trends by department, salary, tenure, etc.
- **Model Metrics**: View model performance metrics (accuracy, precision, recall, F1, ROC-AUC)
- **Responsive UI**: Mobile-friendly design with dark/light mode support
- **REST API**: Complete API for programmatic access

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts
- **Backend**: FastAPI, SQLAlchemy ORM, Pydantic
- **Database**: PostgreSQL (production), SQLite (dev)
- **ML**: Python, scikit-learn/XGBoost, pandas, joblib
- **Deployment**: Render.com
- **Version Control**: Git

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive Swagger API documentation.

## Deployment

See [DEPLOY.md](DEPLOY.md) for comprehensive deployment instructions to Render.

## Development Progress

See [PROGRESS.md](PROGRESS.md) for detailed build log with checkpoints and any rollbacks.

## License

MIT
"# employee-attrition-prediction" 
