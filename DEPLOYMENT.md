# Deployment Guide for Render.com

This guide will help you deploy the Jokes Streamer application to Render.com.

## Prerequisites

1. A [GitHub](https://github.com) account
2. A [Render.com](https://render.com) account (free)
3. This repository pushed to GitHub

## Deployment Steps

### Quick Deploy (Using Blueprint)

The easiest way to deploy is using the `render.yaml` blueprint:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New"** → **"Blueprint"**
   - Connect your GitHub account if not already connected
   - Select this repository
   - Render will detect `render.yaml` and show you the services it will create:
     - PostgreSQL Database (`jokes-database`)
     - Backend Web Service (`jokes-backend`)
     - Frontend Static Site (`jokes-frontend`)
   - Click **"Apply"**

3. **Wait for Deployment**
   - Render will create all services automatically
   - Database will be created first
   - Backend will deploy and connect to the database
   - Frontend will build and deploy
   - This can take 5-10 minutes

4. **Access Your App**
   - Once deployed, click on `jokes-frontend` service
   - You'll see your live URL (e.g., `https://jokes-frontend.onrender.com`)
   - Click it to see your app running!

### Manual Deploy (Step by Step)

If you prefer manual setup or the blueprint doesn't work:

#### 1. Create PostgreSQL Database

1. In Render Dashboard, click **"New"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `jokes-database`
   - **Database**: `jokes_db`
   - **User**: `jokes_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
3. Click **"Create Database"**
4. Wait for it to provision (1-2 minutes)
5. Copy the **Internal Database URL** (we'll use this for the backend)

#### 2. Deploy Backend

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `jokes-backend`
   - **Region**: Same as database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty
   - **Environment**: **Docker**
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Docker Build Context Directory**: `./backend`
   - **Plan**: Free
4. **Environment Variables**:
   - Click **"Add Environment Variable"**
   - Key: `DATABASE_URL`
   - Value: Click **"Add from Database"** and select `jokes-database`
5. Click **"Create Web Service"**
6. Wait for deployment (3-5 minutes)
7. Once deployed, note your backend URL (e.g., `https://jokes-backend.onrender.com`)

#### 3. Deploy Frontend

1. Click **"New"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `jokes-frontend`
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
4. **Environment Variables**:
   - Click **"Add Environment Variable"**
   - Key: `REACT_APP_BACKEND_URL`
   - Value: Your backend URL from step 2 (e.g., `https://jokes-backend.onrender.com`)
5. Click **"Create Static Site"**
6. Wait for build and deployment (3-5 minutes)
7. Your app is now live! Click the URL to access it

## Troubleshooting

### Backend won't start

1. Check the logs in the Render dashboard
2. Verify `DATABASE_URL` is set correctly
3. Make sure the database is in "Available" status
4. Check that the Dockerfile path is correct: `./backend/Dockerfile`

### Frontend shows error connecting to backend

1. Verify `REACT_APP_BACKEND_URL` is set to your backend URL
2. Make sure the backend is deployed and running
3. Check CORS is enabled in the backend (it is by default)
4. Trigger a redeploy of the frontend after backend is ready

### Database connection errors

1. Render provides the database URL in the format `postgres://...`
2. Our code automatically converts it to `postgresql://...` (required by psycopg2)
3. Check the backend logs to see the actual error

### Free tier limitations

- Services on the free tier spin down after 15 minutes of inactivity
- First request after spindown will take 30-60 seconds
- Database free tier has 90-day expiration
- 100 GB bandwidth per month

## Monitoring

- **Backend Logs**: Go to `jokes-backend` → Logs tab
- **Database**: Go to `jokes-database` → Info tab for connection details
- **Frontend**: Static sites don't have runtime logs, check build logs

## Updating Your App

When you push changes to GitHub:

1. Backend will automatically redeploy
2. Frontend will automatically rebuild and redeploy
3. Database schema changes require manual migration

## Environment Variables Reference

### Backend
- `DATABASE_URL`: PostgreSQL connection string (auto-set from database)
- `PORT`: HTTP server port (auto-set by Render, default: 10000)
- `GRPC_PORT`: gRPC server port (optional, default: 50051)

### Frontend
- `REACT_APP_BACKEND_URL`: Backend HTTP API URL (must be set manually)

## Cost

All services use the **free tier**:
- PostgreSQL: Free (90 days, then $7/month)
- Backend Web Service: Free (with spindown)
- Static Site: Free

## Next Steps

- Set up a custom domain
- Enable automatic deployments on push
- Set up health check alerts
- Upgrade to paid tiers for production use (no spindown)
