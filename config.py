from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.account import account_bp
from routes.employee import employee_bp
from routes.production import production_bp
from extensions import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True, expose_headers=["Authorization"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/esteio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "secret_key"
jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(production_bp, url_prefix='/production')
app.register_blueprint(employee_bp, url_prefix='/employee')

from routes.account import account
from routes.auth import auth
from routes.production import production
from routes.employee import employee