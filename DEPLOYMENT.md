# Deployment Guide

This project is configured for deployment on **Render** (backend) and **Vercel** (frontend).

## Prerequisites

- Render account (https://render.com)
- Vercel account (https://vercel.com)
- MongoDB Atlas account (https://www.mongodb.com/cloud/atlas)
- GitHub repository connected to both services

## Environment Variables

Create secrets for the following environment variables on both platforms:

### Render (Backend)
- `MONGO_URL` - MongoDB connection string
- `DB_NAME` - Database name (e.g., `ceo_db`)
- `ENVIRONMENT` - Set to `production`

### Vercel (Frontend)
- `REACT_APP_API_URL` - Backend API URL (e.g., `https://ceo-backend.onrender.com`)

## Backend Deployment (Render)

### Option 1: Using render.yaml (Recommended)
1. Push the `render.yaml` file to your GitHub repository
2. Go to https://render.com/dashboard
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Select the `render.yaml` file
6. Fill in the required environment variables
7. Click "Deploy"

### Option 2: Manual Deployment
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Choose the repository
5. Set the following:
   - **Name**: `ceo-backend`
   - **Runtime**: `Docker`
   - **Branch**: `main`
   - **Build Command**: (leave empty, uses Dockerfile)
   - **Start Command**: (leave empty, uses Dockerfile)
6. Add environment variables:
   - `MONGO_URL`
   - `DB_NAME`
   - `ENVIRONMENT=production`
7. Click "Create Web Service"

## Frontend Deployment (Vercel)

### Option 1: Using Vercel CLI
```bash
cd frontend
npm install -g vercel
vercel --prod
```

### Option 2: Using Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Select "Import Git Repository"
4. Choose your GitHub repository
5. Set the following:
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
6. Add environment variables:
   - `REACT_APP_API_URL` - Set to your Render backend URL
7. Click "Deploy"

## Post-Deployment

After deployment:

1. Test the backend API:
```bash
curl https://ceo-backend.onrender.com/health
```

2. Update the frontend environment variable with the backend URL

3. Test the full application flow

## Monitoring

- **Render**: Check logs at https://render.com/dashboard
- **Vercel**: Check deployments at https://vercel.com/dashboard

## Troubleshooting

### Backend not starting
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure MongoDB URL is correct

### Frontend build fails
- Check build logs in Vercel
- Run `npm run build` locally to debug
- Verify `REACT_APP_API_URL` is set correctly

### CORS errors
- Update CORS settings in `backend/server.py`
- Add frontend URL to allowed origins
