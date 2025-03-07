from flask import Blueprint, jsonify
from extensions import db
from models.employee import Employee

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/listafuncionario', methods=['GET'])
def list_employee():
    employees = Employee.query.all()
    employees_list = [employee.to_dict() for employee in employees]
    return jsonify({'employees': employees_list})