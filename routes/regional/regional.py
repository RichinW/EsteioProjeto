from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from models.vs import VS
from models.regional import Regional
from functions.utils import process_message
import datetime
from schema import VSSchema, ProductionSchema
from extensions import db

regional_bp = Blueprint('regional', __name__)


@regional_bp.route('/listaregional/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_regional(min, max):
    query = Regional.query

    total_items = query.count()

    regionais = query.offset(min).limit(max - min).all()

    regional_list = [regional.to_dict() for regional in regionais]

    return jsonify({'regionais': regional_list, 'total_items': total_items})

@regional_bp.route('/listaregional', methods=['GET'])
@jwt_required()
def list_all_regional():
    regionais = Regional.query.all()
    regional_list = [regional.to_dict() for regional in regionais]
    return jsonify({'regionais': regional_list})


@regional_bp.route('/listaregional/<int:id>', methods=['GET'])
@jwt_required()
def get_highways_by_regional(id):
    regional = Regional.query.get(id)
    if not regional:
        return {'error': 'Regional não encontrada'}, 404
    regional_list = [highway.to_dict() for highway in regional.highways]
    return jsonify({'regionais': regional_list})