from app.init import app

from app.user import user_bp
from app.auth import auth_bp
from app.group import group_bp
from app.message import message_bp

# Register routes
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(group_bp, url_prefix='/api')
app.register_blueprint(message_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)