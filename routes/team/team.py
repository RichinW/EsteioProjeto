from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import OperationalError
from models.employee import Employee
from models.team import Team
from schema import TeamSchema
from extensions import db

team_bp = Blueprint('team', __name__)

@team_bp.route('/listatime/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_team(min, max):
    query = Team.query

    total_items = query.count()

    teams = query.offset(min).limit(max - min).all()

    team_list = [team.to_dict() for team in teams]

    return jsonify({'teams': team_list, 'total_items': total_items})

@team_bp.route('/listatime', methods=['GET'])
@jwt_required()
def list_all_team():
    teams = Team.query.all()
    team_list = [team.to_dict() for team in teams]
    return jsonify({'teams': team_list})

@team_bp.route("/cadastrotime", methods=['POST'])
@jwt_required()
def register_team():
    team_data = request.get_json()

    team_schema = TeamSchema()

    try:
        validated_data = team_schema.load(team_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        new_team = Team(
            id_employee_one=validated_data["id_employee_one"],
            id_employee_two=validated_data["id_employee_two"],
        )

        db.session.add(new_team)
        db.session.commit()

        return jsonify({"message": "Time cadastrado com sucesso!"}), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

@team_bp.route("/deletetime/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_team(id):
    team = Team.query.get(id)

    if team:
        db.session.delete(team)
        db.session.commit()

        return jsonify({"message": "Time deletado com sucesso!"})
    else:
        return jsonify({"message": "Erro ao deletar time"})
