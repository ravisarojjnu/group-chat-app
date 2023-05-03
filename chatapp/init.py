from flask import Flask,send_from_directory
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="SECRET_KEY"
db = SQLAlchemy(app)


# Initialize Swagger UI blueprint
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Chat API'
    }
)
@app.route("/api/swagger.json")
def specs():
    return send_from_directory(os.getcwd()+"/chatapp", "swagger.json")
# Register Swagger UI blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
