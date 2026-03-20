#!/bin/bash

echo "Setting up Movie API..."

# create a virtual environment
python3 -m venv .venv

# activate environment
echo "Activating evironment..."
source .venv/bin/activate

# install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# run alembic migrations
echo "Updating alembic"
alembic upgrade head

#load dataset
echo "Seeding database..."
python -m app.etl.download_dataset

echo "MovieAPI initialised sucessfully."

#start server
echo "Starting server..."
uvicorn app.main:app --reload