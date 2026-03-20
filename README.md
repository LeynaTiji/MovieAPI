# MovieAPI
A RESTful movie API that provides movie recommendation endpoints using Anthropic Api, genre trend analytics and semantic analysis on reviews to make an informed and robust movie software.

## Live Deployment
https://overflowing-success-production-57c0.up.railway.app/
### Access Api Docs
https://overflowing-success-production-57c0.up.railway.app/docs


## Features
- Full CRUD operations for reviews
- JWT authentication for protected endpoints
- AI-powered movie recommendations using Anthropic
- Sentiment analysis of critic reviews using TextBlob
- Genre trend informations and decade popularity
- MCP compatible for AI assistant integration

## Tech Stack
- **FastAPI** — API framework
- **SQLAlchemy** — ORM and database management
- **SQLite** — database
- **TextBlob** — sentiment analysis
- **Anthropic AI** — AI recommendations
- **JWT** — authentication
- **Alembic** — database migrations
- **pytest** — testing


### How to initiate set up
##### On Windows
./setup.bat

##### on Mac/Linux
chmod +x setup.sh
./setup.sh

#### To run API
uvicorn app.main:app --reload

### To run unit tests
pytest
### To see the name of every individual test
pytest tests/ -v