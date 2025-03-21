from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from extensions import db
from schema import MissionSchema
from models.mission import Mission

mission_bp = Blueprint('mission', __name__)

@mission_bp.route('/listamissao/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_mission(min, max):
    query = Mission.query

    total_items = query.count()

    missions = query.offset(min).limit(max - min).all()

    mission_list = [mission.to_dict() for mission in missions]

    return jsonify({'missions': mission_list, 'total_items': total_items})

@mission_bp.route('/listamissao', methods=['GET'])
@jwt_required()
def list_all_mission():
    missions = Mission.query.all()
    mission_list = [mission.to_dict() for mission in missions]
    return jsonify({'missions': mission_list})

@mission_bp.route('/listamissao/<int:min>', methods=['GET'])
@jwt_required(id)
def list_my_mission():
    missions = Mission.query.all()
    mission_list = [mission.to_dict() for mission in missions]
    return jsonify({'missions': mission_list})

@mission_bp.route("/cadastromissao", methods=['POST'])
@jwt_required()
def register_mission():
    mission_data = request.get_json()

    mission_schema = MissionSchema()

    try:
        validated_data = mission_schema.load(mission_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        new_mission = Mission(
            name=validated_data["name"],
            audit=validated_data["audit"],
            activity=validated_data["activity"],
            type=validated_data["type"],
            km_start=validated_data["km_start"],
            km_end=validated_data["km_end"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            regional_id=validated_data["id_regional"],
            team_id=validated_data["id_team"],
            observation=validated_data["observation"],
        )

        db.session.add(new_mission)
        db.session.commit()

        return jsonify({"message": "Missão cadastrada com sucesso!"}), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

@mission_bp.route("/deletemissao/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_mission(id):
    mission = Mission.query.get(id)

    if mission:
        db.session.delete(mission)
        db.session.commit()

        return jsonify({"message": "Missão deletada com sucesso!"})
    else:
        return jsonify({"message": "Erro ao deletar missão"})
