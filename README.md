# MovieAPI
An API that provides movie recommendation endpoints, genre trend analysis, rating distribution information and movie similarity to help create informed movie recommendation software.


### How to install the virtual environment using the requirements file
chmod +x setup.sh
./setup.sh

#### To run API
uvicorn app.main:app --reload

### To run unit tests
pytest
### To see the name of every individual test
pytest tests/ -v
