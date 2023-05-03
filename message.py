from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models import  Group, Message, User,MessageLike
from auth import token_required
message_bp = Blueprint('message', __name__)

# Send message to group
@message_bp.route('/groups/<int:group_id>/messages', methods=['GET'])
@token_required
def get_group_message(current_user,group_id):
    user_id=current_user.id
    group = Group.query.get(group_id)
   
    if not group:
        return make_response(jsonify({"error": "Group not found"}), 404)
    
    if user_id not in set([m.user_id for m in group.memberships]):
        return make_response(jsonify({"error": "User is not part of this group"}), 400)

    messages = Message.query.filter(Message.group_id==group_id).order_by(Message.created_date.desc()).all()

    return make_response(jsonify({"messages":[{"id":m.id,"text":m.text,"user_id":m.user_id,"group_id":m.group_id,"created_date":m.created_date,"likes":[l.user_id for l in m.likes]}for m in messages]}), 200)

# Send message to group
@message_bp.route('/groups/<int:group_id>/messages', methods=['POST'])
@token_required
def send_group_message(current_user,group_id):
    
    data = request.get_json()
    content = data.get('text')

    if not content:
        return make_response(jsonify({"error": "Missing message content"}), 400)
    
    
    group = Group.query.get(group_id)

    if not group:
        return make_response(jsonify({"error": "Group not found"}), 404)

    message = Message(text=content, user_id=current_user.id, group_id=group_id)
    db.session.add(message)
    db.session.commit()

    return make_response(jsonify({"success": f"Message sent to group {group.name}"}), 201)

# Like message
@message_bp.route('/groups/<int:group_id>/messages/<int:message_id>/like', methods=['POST'])
@token_required
def like_message(current_user,group_id, message_id):
    current_user_id = current_user.id
    current_user = User.query.get(current_user_id)

    message = Message.query.filter_by(id=message_id, group_id=group_id).first()

    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    if current_user_id in set([ml.user_id for ml in message.likes]):
        return make_response(jsonify({"error": "User already liked message"}), 400)
    messgeLike=MessageLike(user_id=current_user_id,message_id=message.id)
    db.session.add(messgeLike)
    db.session.commit()

    return make_response(jsonify({"success": "Message liked"}), 200)