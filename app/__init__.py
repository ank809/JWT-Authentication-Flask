from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import timedelta
from flask_jwt_extended import JWTManager
from config import SECRET_KEY, MONGO_URI, JWT_SECRET_KEY

app= Flask(__name__)
jwt= JWTManager(app)
userCount=0

app.config['SECRET_KEY']=SECRET_KEY
app.config['MONGO_URI']=MONGO_URI
app.config['JWT_SECRET_KEY']=JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(minutes=15)

mongo=PyMongo(app)
revoked_tokens_db= mongo.db['revoked_tokens']


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    data= jwt_data['sub']
    user= mongo.db.jwt_database.find_one({"username":data})
    return user

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"error":"Token has been expired"}),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error":"Invalid token"}),401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"Error":"Request does not contain valid token", "error":"Unauthorized token"}),401


# defining additional claims
@jwt.additional_claims_loader
def add_claims(identity):
    if identity=="Ashish":
        return {"role":"admin"}
    return {"role":"users"}


# Checks if the token is revoked or not 
@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti= jwt_data['jti']
    return revoked_tokens_db.find_one({"jti":jti})

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return {
        "msg":"user has been logged out",
        "error":"token has been revoked"
    }

from app.routes import user, auth
