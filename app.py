from init import app
# Register routes

from user import user_bp
from auth import auth_bp
from group import group_bp
from message import message_bp
from flask import Flask, send_from_directory
import os
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(group_bp, url_prefix='/api')
app.register_blueprint(message_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)