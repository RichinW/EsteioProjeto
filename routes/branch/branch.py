from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schema import EmployeeSchema

from extensions import db
from models.branch import Branch

branch_bp = Blueprint('branch', __name__)

@branch_bp.route('/listafilial', methods=['GET'])
@jwt_required()
def list_all_branch():
    branches = Branch.query.all()
    branches_list = [branch.to_dict() for branch in branches]
    return jsonify({'branches': branches_list})