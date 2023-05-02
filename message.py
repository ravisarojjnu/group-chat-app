from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models import  Group, Message, User

message_bp = Blueprint('message', __name__)

# Send message to group
@message_bp.route('/groups/<int:group_id>/messages', methods=['POST'])
@jwt_required
def send_group_message(group_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()
    content = data.get('content')

    if not content:
        return make_response(jsonify({"error": "Missing message content"}), 400)

    group = Group.query.get(group_id)

    if not group:
        return make_response(jsonify({"error": "Group not found"}), 404)

    message = Message(content=content, user=current_user, group=group)
    db.session.add(message)
    db.session.commit()

    return make_response(jsonify({"success": f"Message sent to group {group.name}"}), 201)

# Like message
@message_bp.route('/groups/<int:group_id>/messages/<int:message_id>/like', methods=['POST'])
@jwt_required
def like_message(group_id, message_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    message = Message.query.filter_by(id=message_id, group_id=group_id).first()

    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    if current_user in message.likes:
        return make_response(jsonify({"error": "User already liked message"}), 400)

    message.likes.append(current_user)
    db.session.commit()

    return make_response(jsonify({"success": "Message liked"}), 200)