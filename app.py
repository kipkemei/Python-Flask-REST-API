from flask import Flask, jsonify, request, Response
from BookModel import *
from settings import *
import json, datetime
from flask_jwt import jwt
from UserModel import User
from functools import wraps

books = Book.get_all_books()

DEFAULT_PAGE_LIMIT = 3  

app.config['SECRET_KEY'] = 'wamlambez254'

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:  
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


# GET /books/page/<int:page_number>
#/books/page/1?limit=100
@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    startIndex = page_number * LIMIT - LIMIT
    endIndex = page_number * LIMIT
    print(startIndex)
    print(endIndex)
    return jsonify({'books': books[startIndex:endIndex]})


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'You need a valid token to view this page.'}), 401
    return wrapper
#
# GETs
#
############################################################################################
#GET /books?<token>
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


# GET /books/<isbn>
    # 2nd parameter passed in url will be stored as 'isbn'
    #   and can then be used as a parameter for the method
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)
#
# POSTS
#
##################################################################################################
# POST /books


@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()

    # sanitize data
    if (validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        # construct response
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        
        return response
    else:   
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 97803948016}"
        }
        # construct response
            # json.dumps() converts our dictionary into json

        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

#        
#PUTs
#
#####################################################################################################
#PUT /boooks/7897410258523696
# {
#     'name': 'Wamlambez',
#     'price': 5.99
# }
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    # sanitize data
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Valid book object must be passed in the request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')

        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)

def valid_put_request_data(request_data):
    if ("name" in request_data 
            and "price" in request_data 
            and "isbn" in request_data):
        return True
    else:
        return False

#
# PATCHs
#
####################################################################################################
# PATCH /books/isbn
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    # sanitize data
    if(not valid_patch_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Valid book object must be passed in the request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')

        return response
    
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
        # TODO: fix this section. Sending a PATCH with a price returns 500
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response

def valid_patch_request_data(request_data):
    if ("name" in request_data 
            or "price" in request_data):
        return True
    else:
        return False


#
# DELETEs
#
##################################################################################################
#DELETE /books/isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if (Book.delete_book(isbn)):
        response = Response("", status=204)
        return response
    else:
        invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number provided was not found, so therefore unable to delete"}
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
        return response


# start server
app.run(debug=True, port=5000)
