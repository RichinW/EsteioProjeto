from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from models.vs import VS
from models.regional import Highway
from functions.utils import process_message
import datetime
from schema import VSSchema, ProductionSchema
from extensions import db


highway_bp = Blueprint('highway', __name__)

@highway_bp.route('/listahighway', methods=['GET'])
@jwt_required()
def list_all_highway():
    highways = Highway.query.all()
    highways_list = [highway.to_dict() for highway in highways]
    return jsonify({'highways': highways_list})