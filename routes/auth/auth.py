from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request, create_access_token
from flask import jsonify, Blueprint
from models.account import Account
from models.employee import Employee
from models.team import Team
from models.mission import Mission
from datetime import datetime, timezone, timedelta
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    return jsonify(logged_in_as=current_user), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_account_info():
    employee_id = get_jwt_identity()

    employee = Employee.query.filter_by(id=employee_id).first()

    if employee:
        missions = Mission.query.join(Team).filter(
            (Team.id_employee_one == employee_id) | (Team.id_employee_two == employee_id)
        ).all()

        missions_data = [mission.to_dict() for mission in missions]

        return jsonify({
            'employee': employee.to_dict(),
            'missions': missions_data
        }), 200
    else:
        return jsonify({"message": "Funcionário não encontrado!"}), 404

@auth_bp.after_request
def refresh_expiring_jwt(response):
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if not identity:
            return response

        exp_timestamp = get_jwt().get("exp")
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))  # Ajuste o tempo como quiser

        if exp_timestamp < target_timestamp:
            new_token = create_access_token(identity=identity)
            response.headers["Authorization"] = f"Bearer {new_token}"

    except Exception as e:
        # Se quiser logar o erro para depuração
        print(f"Erro ao renovar token: {e}")
    return response