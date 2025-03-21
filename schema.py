from marshmallow import Schema, fields, validate, ValidationError, validates_schema, post_load
import re
from marshmallow_enum import EnumField
from models.enums import StatusVerification

class CPFField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = re.sub(r'\D', '', value)

        if len(value) != 11:
            raise ValidationError("CPF deve ter 11 dígitos")

        return value

def validate_phone(value):
    pattern = r'^\+?(\d{2})?(\d{4,5})\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError("Número de telefone inválido.")

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("A senha deve ter no mínimo 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("A senha deve conter pelo menos uma letra minúscula.")
    if not re.search(r"\d", password):
        raise ValidationError("A senha deve conter pelo menos um número.")
    if not re.search(r"[\W_]", password):
        raise ValidationError("A senha deve conter pelo menos um caractere especial.")
    return password


class TeamSchema(Schema):
    id_employee_one = fields.Int(required=True)
    id_employee_two = fields.Int(required=False)

class AccountRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=False)
    password = fields.String(required=True, validate=validate_password)
    confirm_password = fields.String(required=True)

    @validates_schema
    def validate_password_confirmation(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("As senhas não coincidem.", field_name="confirm_password")


class AccountLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class VSSchema(Schema):
    id = fields.Int(dump_only=True)
    highway = fields.Str(required=True)
    km = fields.Float(required=True)
    route = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    regional = fields.Str(required=True)
    sense = fields.Str(required=True)
    side = fields.Str(required=True)
    date_register = fields.Date(required=True)
    id_account_register = fields.Int(required=True)
    board_type = fields.Str(required=True)
    sheet_material = fields.Str(required=True)
    type_of_support = fields.Str(required=True)
    plate_code = fields.Str(required=True)

    account_register = fields.Nested('Account_Schema', dump_only=True)


class ProductionSchema(Schema):

    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    mission_id = fields.Int(required=True)
    highway_id = fields.Int(required=True)
    km_start = fields.Float(required=True)
    km_end = fields.Float(required=True)
    extension = fields.Float(dump_only=True)
    total_elements = fields.Int(required=True)
    state_highway = fields.Str(required=True, validate=validate.Length(max=100))
    observation = fields.Str(missing=None)
    verification_status = EnumField(StatusVerification, by_value=True, missing=None)
    verification_observation = fields.Str(missing=None)

    @staticmethod
    def calculate_extension(km_start, km_end):
        return km_end - km_start

    def post_load(self, data, **kwargs):
        km_start = data.get('km_start')
        km_end = data.get('km_end')
        if km_start is not None and km_end is not None:
            data['extension'] = self.calculate_extension(km_start, km_end)
        return data

class EmployeeSchema(Schema):
    name = fields.String(required=True)
    date_of_birth = fields.Date(required=True)
    cpf = CPFField()
    phone = fields.String(required=False, validate=validate_phone)
    phone_contact = fields.String(required=False, validate=validate_phone)
    id_account = fields.Int(required=True)

class MissionSchema(Schema):
    name = fields.String(required=True)
    audit = fields.Int(required=True)
    activity = fields.String(required=True)
    type = fields.String(required=True)
    km_start = fields.Float(required=True)
    km_end = fields.Float(required=True)
    start_date = fields.String(required=True)
    end_date = fields.String(required=True)
    id_regional = fields.Int(required=True)
    id_team = fields.Int(required=True)
    observation = fields.String(required=False)
