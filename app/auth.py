from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from .models import User
import jwt
from datetime import datetime, timedelta
from flask import current_app
from functools import wraps
auth_bp = Blueprint('auth', __name__)




@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        # Generate JWT token
        token = jwt.encode({'user_id': str(user.id),'exp': datetime.utcnow() + timedelta(hours=1)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'User authenticated successfully',"api_key":token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Remove token from client-side storage (e.g., cookies or local storage)
    response = jsonify({'message': 'User logged out successfully'})
    response.delete_cookie('Authorization')
    return response, 200
    

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
         
        if not 'Authorization' in request.headers:
            return jsonify({'message': 'no Authorization header found'}), 401
        words = request.headers['Authorization'].split(" ")
        if words[0]!="Bearer":
            return jsonify({'message': 'Unknown Authorization method other than Bearer'}), 401

        if len(words)<2 and not words[1]:
            return jsonify({'message': 'Token is missing'}), 401
        token= words[1]
        try:
            print(token)
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return func(current_user, *args, **kwargs)

    return decorated

def admin_required(func):
    @wraps(func)
    def decorated(current_user,*args, **kwargs):
        try:
            if not current_user:
                return jsonify({'message': 'login user is not exist'}), 404
            if not current_user.is_admin:
                return jsonify({'message': 'user is not admin'}), 401
        except:
            return jsonify({'message': 'unknown error'}), 500

        return func(current_user, *args, **kwargs)

    return decorated