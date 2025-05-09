#!/bin/bash

# Run the schema.py to create the database
python -m schema

# Start the FastAPI server
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
