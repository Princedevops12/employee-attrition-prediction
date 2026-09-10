# Deployment Guide - Employee Attrition Prediction

This guide provides step-by-step instructions to deploy the Employee Attrition Prediction application to Render.com.

## Prerequisites

- GitHub account with the repository pushed
- Render.com account (sign up at https://render.com)
- PostgreSQL database (Render managed or external)

## Deployment Architecture

The application will be deployed as:
1. **Frontend**: Static site (React/Vite build) or Web Service
2. **Backend**: Web Service (FastAPI with Gunicorn)
3. **Database**: Render PostgreSQL instance
4. **Environment**: Configuration via environment variables

## Step-by-Step Deployment

### Step 1: Prepare Repository

1. Ensure all changes are committed:
   ```bash
   git status
   git add .
   git commit -m "Ready for deployment"
   ```

2. Push to GitHub:
   ```bash
   git push origin main
   ```

3. Create `.env.example` in the backend directory (add to git):
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/attrition_db
   API_BASE_URL=http://localhost:8000
   CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
   ENVIRONMENT=development
   ```

### Step 2: Create Render PostgreSQL Database

1. Log in to Render.com
2. Click "New" → "PostgreSQL"
3. Configure:
   - Name: `employee-attrition-db`
   - Database: `attrition_db`
   - User: `attrition_user`
   - Region: Choose closest to users
   - PostgreSQL Version: 14+
4. Click "Create Database"
5. Copy the Internal Database URL (you'll need this)

### Step 3: Deploy Backend Service

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `employee-attrition-api`
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt && cd backend && alembic upgrade head
     ```
   - **Start Command**: 
     ```bash
     cd backend && gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
     ```
   - **Region**: Same as database
   - **Plan**: Free or Starter

4. Set Environment Variables:
   - `DATABASE_URL`: (paste the Internal Database URL from PostgreSQL)
   - `API_BASE_URL`: (will be provided by Render)
   - `CORS_ORIGINS`: `["https://your-frontend-domain.onrender.com"]`
   - `ENVIRONMENT`: `production`
   - `PYTHONUNBUFFERED`: `1`

5. Click "Create Web Service"
6. Wait for deployment to complete (~5-10 minutes)
7. Note the service URL (e.g., `https://employee-attrition-api.onrender.com`)

### Step 4: Deploy Frontend Service

#### Option A: Static Site (Recommended)

1. Click "New" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `employee-attrition-ui`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Region**: Same as backend
4. Set Environment Variables in frontend/.env or via Render:
   - `VITE_API_BASE_URL`: `https://employee-attrition-api.onrender.com`
5. Click "Create Static Site"
6. Wait for deployment (~3-5 minutes)
7. Note the site URL

#### Option B: Web Service (if you need SSR or additional features)

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `employee-attrition-ui`
   - **Environment**: Node
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `cd frontend && npm run preview`
   - **Region**: Same as backend
4. Set Environment Variable:
   - `VITE_API_BASE_URL`: (your API URL)
5. Click "Create Web Service"

### Step 5: Connect Frontend to Backend

1. Update the backend's `CORS_ORIGINS` environment variable:
   - Go to the Backend Web Service settings
   - Edit environment variables
   - Set `CORS_ORIGINS` to include the frontend URL:
     ```
     ["https://employee-attrition-ui.onrender.com"]
     ```
   - Save and the service will redeploy

2. Update the frontend's API base URL:
   - If using Static Site, update `VITE_API_BASE_URL` in build environment
   - If using Web Service, update the environment variable
   - Redeploy the frontend

### Step 6: Verify Deployment

1. Visit the frontend URL in your browser
2. Navigate to the prediction form
3. Submit a test prediction
4. Verify:
   - Form submits without errors
   - Backend processes the request
   - Database stores the prediction
   - Result displays correctly on frontend
5. Check the backend health:
   ```bash
   curl https://your-backend-url.onrender.com/api/health
   ```
6. View API docs (if exposed):
   ```
   https://your-backend-url.onrender.com/docs
   ```

### Step 7: Monitor Deployment

- **Logs**: Go to Service → "Logs" tab to see real-time logs
- **Metrics**: View CPU, memory, disk usage in the Dashboard
- **Alerts**: Set up notifications in Account Settings

## Troubleshooting

### Database Connection Failed
- Check `DATABASE_URL` is correctly set
- Verify Render PostgreSQL is running
- Ensure firewall allows Render IP

### CORS Errors in Frontend
- Check backend `CORS_ORIGINS` includes frontend URL
- Restart backend service after updating environment variables

### Build Failures
- Check build logs in Render dashboard
- Verify all dependencies are in requirements.txt and package.json
- Ensure Python/Node versions are compatible

### Slow Deployments
- Upgrade to a higher plan if hitting timeout limits
- Optimize dependencies (remove unused packages)
- Use production builds and not development dependencies

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `API_BASE_URL` | Yes | Base URL for the API |
| `CORS_ORIGINS` | Yes | Allowed frontend origins (JSON array) |
| `ENVIRONMENT` | Yes | `production` or `development` |
| `PYTHONUNBUFFERED` | No | Set to `1` to see real-time logs |

## Rollback

To rollback a deployment:

1. Go to the Web Service in Render
2. Click "Deploys" tab
3. Select a previous successful deployment
4. Click "Rollback"

## Support

- Render Docs: https://render.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- React Build: https://vitejs.dev/guide/build.html

---

**Last Updated**: [Current Date]
**Status**: Production Ready
