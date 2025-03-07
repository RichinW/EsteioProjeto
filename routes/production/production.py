from flask import jsonify, Blueprint, request
from marshmallow import ValidationError
from models.vs import VS
from models.production import Production
from functions.utils import process_message
import datetime
from schema import VSSchema
from extensions import db

production_bp = Blueprint('production', __name__)

@production_bp.route('/listaproducao', methods=['GET'])
def list_production():
    productions = Production.query.all()
    production_list = [production.to_dict() for production in productions]
    return jsonify({'productions': production_list})


@production_bp.route('/cadastroproducaoweb', methods=['POST'])
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
def register_production_app():
    data = request.get_json()

@production_bp.route('/adicionarverificacao', methods=['POST'])
def register_verification():
    pass

@production_bp.route('/listasv', methods=['GET'])
def list_sv():
    svs = VS.query.all()
    svs_list = [sv.to_dict() for sv in svs]
    jsonify({'sv': svs_list})

@production_bp.route('/adicionarsv', methods=['POST'])
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