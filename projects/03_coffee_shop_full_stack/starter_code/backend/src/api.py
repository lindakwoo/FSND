import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# undo comments below to clear all data in database 
# and then seed it with two drinks:

# db_drop_and_create_all()
# recipe = [{"color": "orange", "name":"orange juice", "parts":1}]
# recipe_str = json.dumps(recipe)
# drink = Drink(title = "Wooster", recipe = recipe_str)
# drink.insert()
# recipe = [{"color": "blue", "name":"blueberries", "parts":2},
# {"color": "yellow", "name":"lemons", "parts":1}]
# recipe_str = json.dumps(recipe)
# drink = Drink(title = "drinkipoo", recipe = recipe_str)
# drink.insert()

# ROUTES

# get '/drinks' requires no authorization and displays 
# drinks upon opening the website.


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = [drink.short() for drink in 
        Drink.query.order_by(Drink.id).all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        })     
    except Exception as e:
        print(e)
        abort(422)     


# get '/drinks-detail' needs authorization and allows 
# user to click on drinks to see details
@app.route('/drinks-detail', methods=["GET"])
@requires_auth('get:drinks-detail')
def get_long_drinks(jwt):
    try:
        drinks = [drink.long() for drink in 
        Drink.query.order_by(Drink.id).all()]
        return jsonify({
            "success": True,
            "drinks": drinks
        })
    except Exception:
        abort(422)      


# post '/drinks' needs authorization and allows user to create 
# new drink and add to database
@app.route('/drinks', methods=["POST"])
@requires_auth('post:drinks')
def create_drink(jwt):
    if request.data:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        Drink.insert(drink)
        new_drink = Drink.query.filter_by(id=drink.id).first()
        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        })
    else:
        abort(422)

# patch '/drinks/<id>' needs authorization and allows user to alter 
# drinks details and save changes to database
@app.route('/drinks/<id>', methods=["PATCH"])
@requires_auth('patch:drinks')
def change_drink(jwt, id):
    if request.data:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        else:
            drink.title = title
            drink.recipe = json.dumps(recipe)
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
    else:
        abort(422)

# delete '/drinks/<id>' needs authorization and allows user to delete 
# a drink from the database
@app.route('/drinks/<id>', methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        else:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
    except Exception:
        abort(422)         

# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422
    

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400


@app.errorhandler(405)
def bad_method(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "wrong method"
        }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "internal server error"
        }), 500


@app.errorhandler(401)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "invalid authorization"
        }), 401


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code
