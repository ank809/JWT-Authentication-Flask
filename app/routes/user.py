from flask import jsonify, request
from flask_jwt_extended import ( jwt_required, 
                        get_jwt_identity, get_jwt, 
                        create_access_token, 
                        decode_token)
from app import mongo, app, revoked_tokens_db
from datetime import datetime


@app.route('/')
def hello():
    return {
        "Message":"Hello",
    }

@app.route('/get_users', methods=['GET'])
@jwt_required()
def get_users():
    claim= get_jwt()
    if claim.get('role')=="admin":
        user_details=[]
        users=mongo.db.jwt_database.find()
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
    current_user= get_jwt_identity()
    return jsonify(logged_in_as=current_user),200

@app.route('/who_am_i', methods=['GET'])
@jwt_required()
def whoami():
    identity= get_jwt_identity()
    # if isTokenRevoked(identity=identity):
    #     return jsonify({"revoked":"your token id is revoked", "identity":identity})
    current_user=get_jwt_identity()
    user= mongo.db.jwt_database.find_one({"username":current_user})
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

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity= get_jwt_identity()
    access_token= create_access_token(identity=identity)
    return({"new_token":access_token})

@app.route('/check_token_expiry', methods=['GET'])
@jwt_required()
def check_token_expiry():
    identity= get_jwt_identity()
    # first this will retrieve the Authorization from the http request and then split using space because the 
    # header is in format Bearer <token> and 1 is used t get the second  element
    jwt_token = request.headers.get('Authorization').split(' ')[1]
    token_payload= decode_token(jwt_token)
    expiration_time= token_payload['exp']
    expiration_datetime= datetime.utcfromtimestamp(expiration_time)
    time_now= datetime.utcnow()
    timeleft= expiration_datetime-time_now

    return jsonify({"username": identity, "time left":str(timeleft)})



@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    identity= get_jwt()
    jti= identity['jti']
    sub= identity['sub']
    revoked_tokens_db.insert_one({"jti":jti, "sub":sub})
    return jsonify({"success":"Logout Successfully"}), 200