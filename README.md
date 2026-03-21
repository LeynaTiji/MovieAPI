# MovieAPI
A RESTful movie API that provides movie recommendation endpoints using Anthropic Api, genre trend analytics and semantic analysis on reviews to make an informed and robust movie software.

## Live Deployment
https://overflowing-success-production-57c0.up.railway.app/

### Access Api Docs
https://overflowing-success-production-57c0.up.railway.app/docs
#### Full PDF version of API Document
[API Documentation](docs/api_documentation.pdf)


## Features
- Full CRUD operations for reviews
- JWT authentication for protected endpoints
- AI-powered movie recommendations using Anthropic
- Sentiment analysis of critic reviews using TextBlob
- Genre trend informations and decade popularity
- MCP compatible for AI assistant integration

## Tech Stack
- **FastAPI** — API framework
- **SQLAlchemy and Psycog** — ORM and database management
- **SQLite** — database
- **TextBlob** — sentiment analysis
- **Anthropic AI** — AI recommendations
- **JWT** — authentication
- **Alembic** — database migrations
- **pytest** — testing


### How to set up locally

##### On Windows
./setup.bat

##### on Mac/Linux
chmod +x setup.sh
./setup.sh

#### Run virtual environment
##### On Windows
.venv\Scripts\activate

##### on Mac/Linux
source .venv/bin/activate

#### To run API, make sure you are in venv
uvicorn app.main:app --reload

#### To set up Anthropic API by creating an api key on Claude Platform
#### Run
copy .env-example .env
#### Then add your own unique api key from Claude and paste it instead of 'your-api-here'
#### You will be able to interact with Claude api through the recommendations endpoint 

### To run unit tests
pytest
### To see the name of every individual test
pytest tests/ -v