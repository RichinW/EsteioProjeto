from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response, Blueprint

from extensions import db
from models.account import Account
from schema import AccountLoginSchema, AccountRegisterSchema
from marshmallow import ValidationError
account_bp = Blueprint('account', __name__)

@account_bp.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()

    login_schema = AccountLoginSchema()

    try:
        validated_data = login_schema.load(login_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    cpf = validated_data['cpf']
    password = validated_data['password']

    account = Account.query.filter_by(cpf=cpf).first()
    if account and account.verification_password(password):
        access_token = create_access_token(identity=account.cpf)
        response = make_response(jsonify({"message": "Login bem-sucedido!"}), 200)
        response.headers['Authorization'] = f'Bearer {access_token}'

        return response
    else:
        return jsonify({"message": "Credenciais invalidas!"}), 401

@account_bp.route("/cadastrousuario", methods=['POST'])
def register_account():
    register_data = request.get_json()

    register_schema = AccountRegisterSchema()

    try:
        validated_data = register_schema.load(register_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_account = Account(
        username=validated_data["username"],
        email=validated_data["email"],
        cpf=validated_data["cpf"],
        password=validated_data["password"]
    )

    db.session.add(new_account)
    db.session.commit()

    return jsonify({"message": "Cadastro realizado com sucesso!"}), 201

@account_bp.route('/listausuario', methods=['GET'])
def list_account():
    accounts = Account.query.all()
    accounts_list = [account.to_dict() for account in accounts]
    return jsonify({'accounts': accounts_list})


