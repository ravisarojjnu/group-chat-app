from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
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
    

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            print(token)
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return func(current_user, *args, **kwargs)

    return decorated