from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, Blueprint
from models.account import Account

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_account_info():
    cpf = get_jwt_identity()

    account = Account.query.filter_by(cpf=cpf).first()

    if account:
        return jsonify(account.to_dict()), 200
    else:
        return jsonify({"message": "Conta não encontrada!"}), 404
