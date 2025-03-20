from extensions import db
from sqlalchemy import Enum
from models.enums import StatusConservation, ConservationObservation

class StateVSPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state_vs_id = db.Column(db.Integer, db.ForeignKey('state_vs.id'), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    photo_type = db.Column(db.String(100), nullable=True)

    def __init__(self, state_vs_id, photo_url, photo_type=None, created_at=None):
        self.state_vs_id = state_vs_id
        self.photo_url = photo_url
        self.photo_type = photo_type

    def to_dict(self):
        return {
            'id': self.id,
            'state_vs_id': self.state_vs_id,
            'photo_url': self.photo_url,
            'photo_type': self.photo_type,
        }


class VS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    highway_id = db.Column(db.Integer, db.ForeignKey('highway.id'), nullable=False)
    highway = db.relationship('Highway')
    km = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    regional_id = db.Column(db.Integer, db.ForeignKey('regional.id'), nullable=False)
    regional = db.relationship('Regional')
    sense = db.Column(db.String(100), nullable=False)
    side = db.Column(db.String(100), nullable=False)
    date_register = db.Column(db.Date, nullable=False)
    id_account_register = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account_register = db.relationship('Account')
    board_type = db.Column(db.String(100), nullable=False)
    sheet_material = db.Column(db.String(100), nullable=False)
    type_of_support = db.Column(db.String(100), nullable=False)
    plate_code = db.Column(db.String(100), nullable=False)

    def __init__(self, highway_id, km, latitude, longitude, regional_id, sense, side,
                 date_register, id_account_register, board_type, sheet_material, type_of_support, plate_code):
        self.highway_id = highway_id
        self.km = km
        self.latitude = latitude
        self.longitude = longitude
        self.regional_id = regional_id
        self.sense = sense
        self.side = side
        self.date_register = date_register
        self.id_account_register = id_account_register
        self.board_type = board_type
        self.sheet_material = sheet_material
        self.type_of_support = type_of_support
        self.plate_code = plate_code

    def to_dict(self):
        return {
            'id': self.id,
            'highway': self.highway.to_dict() if self.highway_id else None,
            'km': self.km,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'regional': self.regional.to_dict() if self.highway_id else None,
            'sense': self.sense,
            'side': self.side,
            'date_register': self.date_register,
            'account_register': self.account_register.to_dict() if self.id_account_register else None,
            'board_type': self.board_type,
            'sheet_material': self.sheet_material,
            'type_of_support': self.type_of_support,
            'plate_code': self.plate_code
        }





class StateVS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audit = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    board_distance = db.Column(db.Float, nullable=False)
    protective_device = db.Column(db.Boolean, nullable=False)
    state_of_conservation = db.Column(Enum(StatusConservation), nullable=False)
    manufacturing_date = db.Column(db.Date, nullable=False)
    conservation_observation = db.Column(Enum(ConservationObservation), nullable=False)
    format = db.Column(db.String(100), nullable=False)
    board_width = db.Column(db.Float, nullable=False)
    board_height = db.Column(db.Float, nullable=False)
    observation = db.Column(db.String(255), nullable=True)
    date_verification = db.Column(db.Date, nullable=False)

    photos = db.relationship('StateVSPhoto', lazy=True)

    employees = db.relationship('Employee', secondary='state_vs_employee', backref='state_vs_association')

    def __init__(self, audit, height, board_distance, protective_device, state_of_conservation,
                 manufacturing_date, conservation_observation, format, board_width, board_height, observation=None):
        self.audit = audit
        self.height = height
        self.board_distance = board_distance
        self.protective_device = protective_device
        self.state_of_conservation = state_of_conservation
        self.manufacturing_date = manufacturing_date
        self.conservation_observation = conservation_observation
        self.format = format
        self.board_width = board_width
        self.board_height = board_height
        self.observation = observation

    def to_dict(self):
        return {
            'id': self.id,
            'audit': self.audit,
            'height': self.height,
            'board_distance': self.board_distance,
            'protective_device': self.protective_device,
            'state_of_conservation': self.state_of_conservation.name,
            'manufacturing_date': str(self.manufacturing_date),
            'conservation_observation': self.conservation_observation.name,
            'format': self.format,
            'board_width': self.board_width,
            'board_height': self.board_height,
            'observation': self.observation,
            'photos': [photo.to_dict() for photo in self.photos],
            'employees': [employee.to_dict() for employee in self.employees]
        }

class StateVSEmployee(db.Model):
    state_vs_id = db.Column(db.Integer, db.ForeignKey('state_vs.id'), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

class ConservationObservation(db.Model):
    value = db.Column(db.String(255), primary_key=True)

    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            'value': self.value
        }