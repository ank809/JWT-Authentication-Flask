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

from app.routes import auth, user 


