from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db, app

@app.route('/')
def hello():
    return "Hello"

@app.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    claim= get_jwt()
    if claim.get('role')=="admin":
        user_details=[]
        users=db.jwt_database.find()
        for user in users:
            details={
                "username":user["username"],
                "email":user["email"],
                "password":user["password"]
            }
            user_details.append(details)
        return jsonify(user_details)
    return jsonify({"Error": "Yor are not authorized to access this"}),401



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user= get_jwt_identity
    return jsonify(logged_in_as=current_user),200

@app.route('/who_am_i', methods=['GET'])
@jwt_required()
def whoami():
    current_user=get_jwt_identity()
    user= db.jwt_database.find_one({"username":current_user})
    if user:
        return jsonify({
            "name":user['username'],
            "email":user['email']
            }),200
    else:
        jsonify({"error":"user not found"})



@app.route('/get_claims', methods=['GET'])
@jwt_required()
def get_claims():
    claims= get_jwt()
    return jsonify({"message":"success","claim":claims})
