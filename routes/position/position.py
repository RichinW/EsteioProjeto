from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schema import EmployeeSchema

from extensions import db
from models.position import Position

position_bp = Blueprint('position', __name__)

@position_bp.route('/listaposicao', methods=['GET'])
@jwt_required()
def list_all_position():
    positions = Position.query.all()
    positions_list = [position.to_dict() for position in positions]
    return jsonify({'positions': positions_list})