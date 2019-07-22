# Python-Flask-REST-API
A Python-Flask-REST-API books application using PostgreSQL db and Flask-SQAlchemy ORM.
Run the App:
$ python app.py
// To create db table from Python intepreter:
>>> from book_model import *
>>> db.create_all()

>>> from user_model import *
>>> db.create_all()
To set this project up locally:
# create new virtual environment, if needed
$ virtualenv venv -p $(which python3)

# activate virtual environment
$ source venv/bin/activate

# install project dependencies
$ pip install -r requirements.txt
