from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schema import EmployeeSchema

from extensions import db
from models.department import Department

department_bp = Blueprint('department', __name__)

@department_bp.route('/listadepartamento', methods=['GET'])
@jwt_required()
def list_all_department():
    departments = Department.query.all()
    departaments_list = [department.to_dict() for department in departments]
    return jsonify({'departments': departaments_list})