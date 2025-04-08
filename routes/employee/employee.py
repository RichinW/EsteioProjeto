from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schema import EmployeeSchema

from extensions import db
from models.employee import Employee

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/listafuncionario/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_employee(min, max):
    query = Employee.query

    total_items = query.count()

    employees = query.offset(min).limit(max - min).all()

    employees_list = [employee.to_dict() for employee in employees]

    return jsonify({'employees': employees_list, 'total_items': total_items})

@employee_bp.route('/listafuncionario', methods=['GET'])
@jwt_required()
def list_all_employee():
    employees = Employee.query.all()
    employees_list = [employee.to_dict() for employee in employees]
    return jsonify({'employees': employees_list})

@employee_bp.route('/cadastrofuncionario', methods=['POST'])
@jwt_required()
def register_employee():
    employee_data = request.get_json()

    employee_schema = EmployeeSchema()

    try:
        validated_data = employee_schema.load(employee_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        new_employee = Employee(
            name=validated_data['name'],
            date_of_birth=validated_data['date_of_birth'],
            cpf=validated_data['cpf'],
            phone=validated_data['phone'],
            phone_contact=validated_data['phone_contact'],
            id_account=validated_data['id_account'],
            id_branch=validated_data['id_branch'],
            id_position=validated_data['id_position'],
            id_department=validated_data['id_department'],
            regular_medication=validated_data['regular_medication'],
            medical_condition=validated_data['medical_condition'],
            allergy=validated_data['allergy'],
            address=validated_data['address'],
            blood_type=validated_data['blood_type'],
            date_of_hire=validated_data['date_of_hire']
        )
        db.session.add(new_employee)
        db.session.commit()

        return jsonify({'message': 'Funcionário cadastrado com sucesso!'}), 201
    except Exception as err:
        return jsonify(err), 400

@employee_bp.route("/deletefuncionario/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    employee = Employee.query.get(id)

    if employee:
        db.session.delete(employee)
        db.session.commit()

        return jsonify({"message": "Funcionário deletado com sucesso!"})
    else:
        return jsonify({"message": "Erro ao deletar funcionário"})