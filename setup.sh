#!/bin/bash

# create a virtual environment
python3 -m venv .venv

# activate environment
source .venv/bin/activate

# upgrade pip
pip install --upgrade pip

# install dependencies
pip install -r requirements.txt

# run alembic migrations
alembic upgrade head

#load dataset
python -m app.etl.download_dataset

echo "MovieAPI initialised sucessfully. To run API use uvicorn app.main:app --reload."