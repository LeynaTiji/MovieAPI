# MovieAPI
An API that provides movie recommendation endpoints, genre trend analysis, rating distribution information and movie similarity to help create informed movie recommendation software.


### How to install the virtual environment using the requirements file
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload