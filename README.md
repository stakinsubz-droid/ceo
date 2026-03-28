# Here are your Instructions

## New AI CEO System Endpoint

The repository now includes a complete orchestrator to run an autonomous commercial product cycle:

- `POST /api/ai/run-complete-launch-cycle?products_per_cycle=3`
- Creates scoped output folders under `/workspaces/ceo/Project_Output/{cycle_id}`
- Runs opportunity scouting, product generation, quality checking, publishing, social content output, and revenue optimization
- Stores mock metadata in MongoDB when `MONGO_URL` is configured

## How to run

1. Start backend:
   - `cd backend`
   - `export APP_ENVIRONMENT=demo`
   - `export MONGO_URL=mongodb://localhost:27017`
   - `export DB_NAME=ceo_ai`
   - `python -m pip install -r requirements.txt`
   - `uvicorn server:app --reload --port 8000`
2. Start frontend:
   - `cd frontend`
   - `npm install`
   - `export REACT_APP_BACKEND_URL=http://localhost:8000`
   - `npm start`

## Project overview

- Backend: FastAPI + modular ai_services
- Frontend: React
- DB: MongoDB (optional)
- Outputs: `Project_Output/` for generated content and tracking

