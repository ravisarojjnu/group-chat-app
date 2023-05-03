from flask import Blueprint, jsonify, request
from .models import  db,User
from .init import db
from werkzeug.security import generate_password_hash
from .auth import token_required,admin_required
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
@token_required
#@admin_required
def create_user(current_user):
    data = request.get_json()
    user = User(username=data['username'], password=generate_password_hash(data['password']), is_admin=data.get('is_admin', False))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(current_user,user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@user_bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'is_admin': user.is_admin} for user in users]), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user,user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'id': user.id, 'username': user.username, 'is_admin': user.is_admin}), 200
    except:
        return jsonify({'message': 'Invalid ID supplied'}), 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user,user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200