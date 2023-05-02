from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db,Group, GroupMembership, User
from auth import token_required
group_bp = Blueprint('group', __name__)

# Create group
@group_bp.route('/groups', methods=['POST'])
@token_required
def create_group(current_user):
    current_user_id = current_user.id
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return make_response(jsonify({"error": "Only admins can create groups"}), 401)

    data = request.get_json()
    name = data.get('name')

    if not name:
        return make_response(jsonify({"error": "Missing group name"}), 400)

    group = Group.query.filter_by(name=name).first()

    if group:
        return make_response(jsonify({"error": "Group already exists"}), 400)

    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    return make_response(jsonify({"success": f"Group {group.name} created"}), 201)

# Delete group
@group_bp.route('/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return make_response(jsonify({"error": "Only admins can delete groups"}), 401)

    group = Group.query.get(group_id)

    if not group:
        return make_response(jsonify({"error": "Group not found"}), 404)

    db.session.delete(group)
    db.session.commit()

    return make_response(jsonify({"success": f"Group {group.name} deleted"}), 200)

# Add member to group
@group_bp.route('/groups/<int:group_id>/members', methods=['POST'])
def add_member_to_group(group_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()
    username = data.get('username')

    if not username:
        return make_response(jsonify({"error": "Missing username"}), 400)

    user = User.query.filter_by(username=username).first()

    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    group = Group.query.get(group_id)

    if not group:
        return make_response(jsonify({"error": "Group not found"}), 404)

    if user in group.memberships:
        return make_response(jsonify({"error": "User already in group"}), 400)

    group_membership = GroupMembership(user=user, group=group)
    db.session.add(group_membership)
    db.session.commit()

    return make_response(jsonify({"success": f"{user.username} added to group {group.name}"}), 201)

# Search for groups by name
@group_bp.route('/groups', methods=['GET'])
def search_groups():
    query = request.args.get('q')

    if not query:
        groups=Group.query.all()
        return make_response(jsonify({"groups": [group.name for group in groups]}), 200)
    groups = Group.query.filter(Group.name.ilike(f'%{query}%')).all()

    return make_response(jsonify({"groups": [group.name for group in groups]}), 200)