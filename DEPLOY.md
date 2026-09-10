# Deployment Guide - Employee Attrition Prediction

Complete guide to deploying the Employee Attrition Prediction application to Render.com.

## Prerequisites

- GitHub account with repository access
- Render.com account (https://render.com)
- Git CLI installed and configured
- Python 3.14+ and Node.js 18+ installed locally

## Architecture Overview

```
┌─────────────────────┐
│   Static Frontend   │
│  (React + Vite)     │
│   render.com/app    │
└──────────┬──────────┘
           │ HTTPS
           ↓
┌─────────────────────┐
│   FastAPI Backend   │
│    (Uvicorn)        │
│  render.com/api/*   │
└──────────┬──────────┘
           │ TCP
           ↓
┌─────────────────────┐
│  PostgreSQL 16      │
│  (Render Managed)   │
└─────────────────────┘
```

## Step 1: Prepare Your Repository

### 1.1 Verify All Code is Committed

```bash
cd "c:\Users\Prince\Desktop\Employee attrition prediction"
git status
git add .
git commit -m "Production ready - all modules complete"
```

### 1.2 Create Environment Template

Ensure `.env.example` exists in backend:

```bash
cat > backend/.env.example << 'EOF'
DATABASE_URL=postgresql://user:password@host:5432/dbname
PYTHON_ENV=production
CORS_ORIGINS=["https://your-frontend-domain.onrender.com"]
EOF
```

### 1.3 Push to GitHub

```bash
git push origin main
# or your default branch
```

## Step 2: Deploy to Render Using render.yaml

### 2.1 Deploy via Blueprint

1. Log in to Render (https://render.com)
2. Click **"New"** → **"Blueprint"**
3. Select **"GitHub"** and authenticate
4. Choose your repository
5. Render will automatically read `render.yaml` and create services

### 2.2 Alternative: Manual Service Creation

If Blueprint deployment fails, create services manually:

#### A. Create PostgreSQL Database

1. Dashboard → **"New"** → **"PostgreSQL"**
2. **Name**: `employee-attrition-db`
3. **Database**: `attrition_prod`
4. **User**: `attrition_admin`
5. **Region**: Oregon (or your preference)
6. **Plan**: Starter (or Pro for production)
7. Click **"Create Database"**
8. **Copy the connection string** (Internal Database URL - safe to use from web services)

#### B. Deploy Backend API

1. Dashboard → **"New"** → **"Web Service"**
2. **Connect**: Select your GitHub repository
3. **Settings**:
   - **Name**: `employee-attrition-api`
   - **Environment**: `Python`
   - **Python Version**: `3.14`
   - **Build Command**:
     ```bash
     pip install -r backend/requirements.txt && cd backend && alembic upgrade head
     ```
   - **Start Command**:
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Starter/Pro (based on needs)
   - **Region**: Oregon

4. **Environment Variables**:
   - `DATABASE_URL`: Paste the PostgreSQL connection string from Step A
   - `PYTHON_ENV`: `production`
   - `CORS_ORIGINS`: `["https://your-frontend-url.onrender.com"]`
   - `PORT`: `10000` (Render-assigned)

5. **Advanced**:
   - **Auto-Deploy**: ON (redeploy on push to main)
   - **Health Check Path**: `/api/health`
   - **Health Check Interval**: 30 seconds
   - **Timeout**: 30 seconds
   - **Max Instances**: 3 (autoscaling)

6. Click **"Create Web Service"**

#### C. Deploy Frontend

1. Dashboard → **"New"** → **"Static Site"**
2. **Connect**: Select your repository
3. **Settings**:
   - **Name**: `employee-attrition-app`
   - **Build Command**:
     ```bash
     cd frontend && npm ci && npm run build
     ```
   - **Publish Directory**: `frontend/dist`
   - **Plan**: Starter/Pro

4. **Environment Variables**:
   - `VITE_API_BASE_URL`: `https://employee-attrition-api.onrender.com`
     (Replace with your actual backend service URL)

5. **Auto-Deploy**: ON

6. Click **"Create Static Site"**

## Step 3: Configure Environment Variables

After all services are created:

### 3.1 Backend Environment

Update Backend service environment variables:

```
DATABASE_URL = postgresql://user:pass@host/dbname
PYTHON_ENV = production
CORS_ORIGINS = ["https://employee-attrition-app.onrender.com"]
```

### 3.2 Frontend Environment

Update Static Site environment variables:

```
VITE_API_BASE_URL = https://employee-attrition-api.onrender.com
```

## Step 4: Verify Deployment

### 4.1 Check Service Status

- Backend: `https://employee-attrition-api.onrender.com/api/health`
  - Expected Response: `{"status": "healthy", ...}`

- Frontend: `https://employee-attrition-app.onrender.com`
  - Should load the prediction form

### 4.2 Test API Endpoints

```bash
# Health Check
curl https://employee-attrition-api.onrender.com/api/health

# Create Employee (test data)
curl -X POST https://employee-attrition-api.onrender.com/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "department": "Sales",
    "job_role": "Sales Executive",
    "age": 45,
    "monthly_income": 5500,
    "years_at_company": 10,
    "job_satisfaction": 3,
    "work_life_balance": 3
  }'

# Get Prediction
curl -X POST https://employee-attrition-api.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "monthly_income": 5500,
    "years_at_company": 10,
    "years_in_current_role": 5,
    "years_with_curr_manager": 3,
    "total_working_years": 15,
    "job_satisfaction": 3,
    "work_life_balance": 3,
    "job_role": "Sales Executive",
    "department": "Sales",
    "distance_from_home": 5,
    "over_time": "No"
  }'
```

## Step 5: Production Considerations

### 5.1 Database Backups

Enable automatic backups in Render PostgreSQL dashboard:

- Backup Frequency: Daily
- Retention Period: 30 days
- Test restore procedures regularly

### 5.2 Monitoring

Monitor application health:

- Render Dashboard: Check logs, metrics
- Health endpoint: Regular pings to `/api/health`
- Error tracking: Implement Sentry/Rollbar for error logging

### 5.3 Performance Optimization

- **Frontend**:
  - Enable gzip compression in Render
  - Use CDN caching for static assets
  - Optimize images and bundle size

- **Backend**:
  - Use connection pooling for database
  - Implement query caching for predictions
  - Scale horizontally with multiple Render Web Service instances
  - Monitor database connection limits

### 5.4 Security Checklist

- [ ] Environment variables are not committed to Git
- [ ] CORS_ORIGINS only includes your frontend domain
- [ ] Database password is unique and strong
- [ ] PostgreSQL requires authentication
- [ ] Enable Render's built-in DDoS protection
- [ ] Use HTTPS everywhere (Render default)
- [ ] Implement rate limiting for API endpoints
- [ ] Regular security updates for dependencies

### 5.5 Cost Management

- **Starter Tier** (Development):
  - Backend: $7/month
  - Frontend: Free
  - Database: $7/month
  - **Total**: ~$14/month

- **Pro Tier** (Production):
  - Backend: $25/month
  - Frontend: $20/month
  - Database: $15/month
  - **Total**: ~$60/month

## Step 6: Continuous Deployment

### 6.1 Auto-Deploy on Push

Both services have auto-deploy enabled. Deployment workflow:

1. Push changes to `main` branch
2. GitHub webhook triggers Render
3. Render rebuilds services
4. New version automatically deployed
5. Old instances gracefully shut down

### 6.2 Manual Deployment

To manually redeploy a service:

1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Monitor deployment progress in logs

## Troubleshooting

### Backend Service Won't Start

**Error**: `ModuleNotFoundError: No module named 'app'`

- **Solution**: Ensure build command includes `cd backend` before uvicorn

**Error**: `Database connection failed`

- **Solution**: Verify DATABASE_URL environment variable is correctly set

**Error**: `Application startup complete` but endpoint returns 502

- **Solution**: Check health endpoint path; backend may still be initializing

### Frontend Shows Blank Page

**Error**: API requests fail with 403/CORS

- **Solution**: Update CORS_ORIGINS on backend to include frontend URL

**Error**: Assets return 404

- **Solution**: Verify `frontend/dist` directory exists in build output

### Database Issues

**Error**: `pgvector extension not found`

- **Solution**: Not needed for this project; vector extension is optional

**Error**: `Connection limit exceeded`

- **Solution**: Implement connection pooling; upgrade to Pro tier

## Rollback Procedure

If deployment causes issues:

1. Render Dashboard → Service → **"Deployment History"**
2. Find previous stable deployment
3. Click **"Deploy"** next to the older version
4. Verify `/api/health` returns success

## Monitoring & Logging

### Real-time Logs

Render Dashboard → Service → **"Logs"**

### Environment Variable Changes

To update environment variables without redeploying:

1. Service Settings → **"Environment"**
2. Edit variables
3. **"Save"** (this triggers restart)

### Performance Metrics

Check Render dashboard for:

- CPU usage
- Memory utilization
- Network bandwidth
- Request rates

## Disaster Recovery

### Database Restore

1. Render PostgreSQL Dashboard → **"Backups"**
2. Select backup timestamp
3. Click **"Restore"**
4. Data restored to new database instance

### Code Rollback

1. Go to GitHub → Releases/Tags
2. Create deployment from previous stable version
3. Push to main branch
4. Render redeploys automatically

## Support & Resources

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://render.com/community
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
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

| Variable           | Required | Description                           |
| ------------------ | -------- | ------------------------------------- |
| `DATABASE_URL`     | Yes      | PostgreSQL connection string          |
| `API_BASE_URL`     | Yes      | Base URL for the API                  |
| `CORS_ORIGINS`     | Yes      | Allowed frontend origins (JSON array) |
| `ENVIRONMENT`      | Yes      | `production` or `development`         |
| `PYTHONUNBUFFERED` | No       | Set to `1` to see real-time logs      |

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
