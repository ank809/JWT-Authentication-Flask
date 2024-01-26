from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from app import mongo, app
from app.models import User, isValidEmail

@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        username= request.json['username']
        password=request.json['password']
        user=mongo.db.jwt_database.find_one({"username":username})
        if username and user['password']==password:
            access_token=create_access_token(identity=username)
            refresh_token= create_refresh_token(identity=username)
            return jsonify({
                "logged in":"successfully logged in",
                "tokens":{
                    "access token":access_token,
                    "refresh token":refresh_token
                }
            }),200
        else:
            return jsonify({
                "error":"invalid username or password"
            }),400
        
        
@app.route('/register', methods=['POST'])
def register():
    if request.method=='POST':
        username=request.json['username']
        email=request.json['email']
        if not isValidEmail(email):
            return jsonify({"error":"Email is not valid"})
        password=request.json['password']
        user= mongo.db.jwt_database.find_one({"username":username})
        if user is not None:
            return jsonify({"exists":"username already exists, choose new one"})
        new= User(username=username,email=email, password=password)
        mongo.db.jwt_database.insert_one(new.to_dict())
        return jsonify({"success":"added successfully"})