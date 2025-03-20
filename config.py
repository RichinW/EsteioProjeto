import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.account import account_bp
from routes.employee import employee_bp
from routes.mission import mission_bp
from routes.production import production_bp
from extensions import db
from routes.regional import regional_bp
from routes.team import team_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True, expose_headers=["Authorization"])

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret")
jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(production_bp, url_prefix='/production')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(mission_bp, url_prefix='/mission')
app.register_blueprint(team_bp, url_prefix='/team')
app.register_blueprint(regional_bp, url_prefix='/regional')

from routes.mission import mission
from routes.team import team
from routes.account import account
from routes.auth import auth
from routes.production import production
from routes.employee import employee
from routes.regional import regional