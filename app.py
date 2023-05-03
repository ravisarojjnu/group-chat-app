from chatapp.init import app

from chatapp.user import user_bp
from chatapp.auth import auth_bp
from chatapp.group import group_bp
from chatapp.message import message_bp

# Register routes
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(group_bp, url_prefix='/api')
app.register_blueprint(message_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)