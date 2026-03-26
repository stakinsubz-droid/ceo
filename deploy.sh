#!/bin/bash

# Deploy CEO to Render and Vercel

set -e

echo "🚀 Starting deployment to Render and Vercel..."

# Check for required tools
command -v git &> /dev/null || { echo "❌ git is required but not installed."; exit 1; }

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $CURRENT_BRANCH"

# Backend deployment to Render
echo ""
echo "📦 Deploying Backend to Render..."

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found!"
    exit 1
fi

# Push code to trigger Render deployment
echo "🔄 Pushing code to GitHub..."
git push origin $CURRENT_BRANCH

echo "✅ Backend push complete. Monitor progress at https://dashboard.render.com/"

# Frontend deployment to Vercel
echo ""
echo "📦 Deploying Frontend to Vercel..."

if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI not found. Installing globally..."
    npm install -g vercel
fi

cd frontend

# Deploy to Vercel
vercel --prod --confirm

cd ..

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Deployment links:"
echo "- Render Dashboard: https://dashboard.render.com/"
echo "- Vercel Dashboard: https://vercel.com/dashboard"
echo ""
echo "⚠️  Remember to:"
echo "1. Set environment variables on both platforms"
echo "2. Configure REACT_APP_API_URL on Vercel with the Render backend URL"
echo "3. Test the health check: curl https://your-render-url/health"
