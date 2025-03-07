from marshmallow import Schema, fields, validate, ValidationError, validates_schema, post_load
import re


class CPFField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = re.sub(r'\D', '', value)

        if len(value) != 11:
            raise ValidationError("CPF deve ter 11 dígitos")

        return value


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


class AccountRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    cpf = CPFField(required=True)
    password = fields.String(required=True, validate=validate_password)
    confirm_password = fields.String(required=True)

    @validates_schema
    def validate_password_confirmation(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("As senhas não coincidem.", field_name="confirm_password")


class AccountLoginSchema(Schema):
    cpf = CPFField(required=True)
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
