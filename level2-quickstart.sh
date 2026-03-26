#!/bin/bash

# 🚀 LEVEL 2 Quick Start Script
# Run this to get your autonomous money-making system going

echo "🔥 LEVEL 2 AUTONOMOUS SYSTEM - QUICK START"
echo "=========================================="
echo ""

# Check if backend is installed
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Backend folder not found!"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
cd backend
pip install requests -q
cd ..

echo "✅ Dependencies ready"
echo ""

# Show configuration
echo "📋 CURRENT CONFIGURATION"
echo "========================"
echo ""

if [ -f ".env" ]; then
    echo "MONGO_URL: $(grep -oP 'MONGO_URL=\K.*' .env | head -c 50)..."
    echo "GUMROAD_TOKEN: $([ -z "$(grep 'GUMROAD_TOKEN' .env)" ] && echo '❌ NOT SET' || echo '✅ SET')"
    echo "TIKTOK_ACCESS_TOKEN: $([ -z "$(grep 'TIKTOK_ACCESS_TOKEN' .env)" ] && echo '❌ NOT SET' || echo '✅ SET')"
    echo "INSTAGRAM_ACCESS_TOKEN: $([ -z "$(grep 'INSTAGRAM_ACCESS_TOKEN' .env)" ] && echo '❌ NOT SET' || echo '✅ SET')"
    echo "TWITTER_BEARER_TOKEN: $([ -z "$(grep 'TWITTER_BEARER_TOKEN' .env)" ] && echo '❌ NOT SET' || echo '✅ SET')"
else
    echo "⚠️  No .env file found. Using .env.example"
fi

echo ""
echo "🎯 QUICK START OPTIONS"
echo "======================="
echo ""
echo "Option 1: Run Single Autonomous Cycle"
echo "  curl -X POST http://localhost:8000/api/run"
echo ""
echo "Option 2: Enable 5 Projects Per Day"
echo "  curl -X POST http://localhost:8000/api/v2/scale/configure?projects_per_day=5"
echo ""
echo "Option 3: Run 5 Projects in Parallel"
echo "  curl -X POST http://localhost:8000/api/v2/scale/run-parallel?num_projects=5"
echo ""
echo "Option 4: Get Revenue Metrics"
echo "  curl http://localhost:8000/api/v2/revenue/all-metrics"
echo ""
echo "Option 5: Get Performance Analysis"
echo "  curl http://localhost:8000/api/v2/improve/analysis"
echo ""
echo "🚀 START BACKEND FIRST:"
echo "  cd /workspaces/ceo"
echo "  uvicorn backend.server:app --reload"
echo ""
echo "📖 Full documentation: LEVEL2_DOCS.md"
echo ""
