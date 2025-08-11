#!/bin/bash

# Activate virtual environment if needed
# source venv/bin/activate

# Run the FastAPI app with live reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

#!/bin/bash
# docker-compose up --build
