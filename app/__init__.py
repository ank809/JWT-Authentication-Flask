from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import SECRET_KEY, MONGO_URI, JWT_SECRET_KEY
app= Flask(__name__)

app.config['SECRET_KEY']=SECRET_KEY
app.config['MONGO_URI']=MONGO_URI
app.config['JWT_SECRET_KEY']=JWT_SECRET_KEY

db=PyMongo(app).db
jwt= JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"error":"Token has been expired"}),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error":"Invalid token"}),401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"Error":"Request does not contain valid token", "error":"Unauthorized token"}),401

from app.routes import user, auth
