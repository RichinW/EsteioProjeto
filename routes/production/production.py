from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from models.vs import VS
from models.production import Production
from functions.utils import process_message
import datetime
from schema import VSSchema, ProductionSchema
from extensions import db

production_bp = Blueprint('production', __name__)


@production_bp.route('/listaproducao/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_production(min, max):
    query = Production.query

    total_items = query.count()

    productions = query.offset(min).limit(max - min).all()

    production_list = [production.to_dict() for production in productions]

    return jsonify({'productions': production_list, 'total_items': total_items})

from flask import request, jsonify

@production_bp.route('/listaproducao/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_filter_production(min, max):
    query = Production.query

    filters = request.get_json()

    if 'type' in filters and filters['type']:
        query = query.filter(Production.type == filters['type'])

    if 'date' in filters and filters['date']:
        query = query.filter(Production.date_register == filters['date'])

    if 'audit' in filters and filters['audit'] is not None:
        query = query.filter(Production.audit == filters['audit'])

    if 'activity' in filters and filters['activity']:
        query = query.filter(Production.activity.ilike(f'%{filters["activity"]}%')) 

    if 'regional' in filters and filters['regional']:
        query = query.filter(Production.regional.ilike(f'%{filters["regional"]}%'))

    if 'highway' in filters and filters['highway']:
        query = query.filter(Production.highway.ilike(f'%{filters["highway"]}%'))

    total_items = query.count()

    productions = query.filter(Production.id >= min, Production.id <= max).all()

    production_list = [production.to_dict() for production in productions]

    return jsonify({'productions': production_list, 'total_items': total_items})


@production_bp.route('/listaproducao/type/<string:type>/<int:min>/<int:max>', methods=['GET'])
@jwt_required()
def list_type_production(type, min, max):
    query = Production.query

    if type:
        query = query.filter(Production.type == type)

    total_items = query.count()

    productions = query.filter(
        Production.id >= min,
        Production.id <= max
    ).all()

    production_list = [production.to_dict() for production in productions]

    return jsonify({'productions': production_list, 'total_items': total_items})


@production_bp.route('/cadastroproducaoweb', methods=['POST'])
@jwt_required()
def register_production_web():
    data = request.get_json()
    production_processed = process_message(data['message'], data['type'])

    for production in production_processed:
        production_object = Production(
            date=datetime.strptime(production['date'], '%d/%m/%Y') if production['date'] else None,
            type=production['type'],
            activity=production['activity'],
            audit=production['audit'],
            team=production['team'],
            highway=production['highway'],
            km_start=production['km_start'],
            km_end=production['km_end'],
            total_elements=production['total_elements'],
            state_highway=production['state_highway'],
            observation=production['observation']
        )

        db.session.add(production_object)

    db.session.commit()

    return jsonify({'mensagem': 'Produção cadastrado com sucesso!'}), 201

@production_bp.route('/cadastroproducaoapp', methods=['POST'])
@jwt_required()
def register_production_app():
    production_data = request.get_json()

    production_schema = ProductionSchema()

    try:
        validated_data = production_schema.load(production_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        new_production = Production(
            date=validated_data['date'],
            mission_id=validated_data['mission_id'],
            highway_id=validated_data['highway_id'],
            km_start=validated_data['km_start'],
            km_end=validated_data['km_end'],
            total_elements=validated_data['total_elements'],
            state_highway=validated_data['state_highway'],
            observation=validated_data.get('observation'),
        )
        db.session.add(new_production)
        db.session.commit()

        return jsonify({'mensagem': 'Produção cadastrado com sucesso!'}), 201
    except Exception as err:
        return jsonify(err), 400

@production_bp.route('/adicionarverificacao', methods=['POST'])
@jwt_required()
def register_verification():
    pass

@production_bp.route('/listasv', methods=['GET'])
@jwt_required()
def list_sv():
    svs = VS.query.all()
    svs_list = [sv.to_dict() for sv in svs]
    jsonify({'sv': svs_list})

@production_bp.route('/adicionarsv', methods=['POST'])
@jwt_required()
def register_sv():
    data = request.get_json()

    vs_schema = VSSchema()

    try:
        validated_data = vs_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_sv = VS(
        highway=validated_data['highway'],
        km=validated_data['km'],
        route=validated_data['route'],
        city=validated_data['city'],
        state=validated_data['state'],
        latitude=validated_data['latitude'],
        longitude=validated_data['longitude'],
        regional=validated_data['regional'],
        sense=validated_data['sense'],
        side=validated_data['side'],
        date_register=validated_data['date_register'],
        id_account_register=validated_data['id_account_register'],
        board_type=validated_data['board_type'],
        sheet_material=validated_data['sheet_material'],
        type_of_support=validated_data['type_of_support'],
        plate_code=validated_data['plate_code']
    )

    db.session.add(new_sv)
    db.session.commit()

    return jsonify({"message": "Cadastro realizado com sucesso!"}), 201