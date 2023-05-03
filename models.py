
from init import db,app
from werkzeug.security import generate_password_hash
import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    memberships = db.relationship('GroupMembership', backref='user', lazy=True)
    likes = db.relationship('MessageLike', backref='user', lazy=True)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    memberships = db.relationship('GroupMembership',cascade="all,delete", backref='group', lazy=True)
    messages = db.relationship('Message', backref='group', lazy=True)

class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    likes = db.relationship('MessageLike', backref='message', lazy=True)

class MessageLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

with app.app_context():
    db.create_all()
    #to add default admin user
    try:
        user = User(username='admin', password=generate_password_hash("admin"), is_admin=True)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        pass


