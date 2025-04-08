from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify, make_response, Blueprint

from extensions import db
from models.account import Account
from models.employee import Employee
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
    username = validated_data['username'].strip()
    password = validated_data['password']
    account = Account.query.filter_by(username=username).first()
    if account and account.verification_password(password):
        employee = Employee.query.filter_by(id_account=account.id).first()
        if employee:
            access_token = create_access_token(identity=str(employee.id))
            response = make_response(jsonify({"message": "Login bem-sucedido!"}), 200)
            response.headers['Authorization'] = f'Bearer {access_token}'
            return response
        else:
            return jsonify({"message": "Funcionário não encontrado para esta conta"}), 404
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401


@account_bp.route("/cadastrousuario", methods=['POST'])
@jwt_required()
def register_account():
    account_data = request.get_json()

    account_schema = AccountRegisterSchema()

    try:
        validated_data = account_schema.load(account_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        new_account = Account(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        db.session.add(new_account)
        db.session.commit()

        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

    except ValidationError as err:
        return jsonify(err.messages), 400


@account_bp.route('/listausuario/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_all_account(min, max):
    query = Account.query

    total_items = query.count()

    accounts = query.offset(min).limit(max - min).all()

    accounts_list = [account.to_dict() for account in accounts]

    return jsonify({'accounts': accounts_list, 'total_items': total_items})


@account_bp.route('/listausuario', methods=['GET'])
@jwt_required()
def list_account():
    accounts = Account.query.all()
    accounts_list = [account.to_dict() for account in accounts]
    return jsonify({'accounts': accounts_list})

@account_bp.route('/listausuario/vazio', methods=['GET'])
@jwt_required()
def list_account_clear():
    accounts = db.session.query(Account).outerjoin(Employee, Account.id == Employee.id_account).filter(Employee.id == None).all()
    accounts_list = [account.to_dict() for account in accounts]
    return jsonify({'accounts': accounts_list})


@account_bp.route("/deleteusuario/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_account(id):
    account = Account.query.get(id)

    if account:
        db.session.delete(account)
        db.session.commit()

        return jsonify({"message": "Usuário deletado com sucesso!"})
    else:
        return jsonify({"message": "Erro ao deletar usuário"})