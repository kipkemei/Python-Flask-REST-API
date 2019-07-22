from flask import Flask 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nyiganet@localhost/booksDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False