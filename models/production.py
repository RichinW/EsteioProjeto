from extensions import db
from sqlalchemy import Enum
from models.enums import StatusVerification
from models.mission import Mission
from models.regional import Highway

class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    mission = db.relationship('Mission')
    highway_id = db.Column(db.Integer, db.ForeignKey('highway.id'), nullable=False)
    highway_obj = db.relationship('Highway')
    km_start = db.Column(db.Float, nullable=False)
    km_end = db.Column(db.Float, nullable=False)
    extension = db.Column(db.Float, nullable=False)
    total_elements = db.Column(db.Integer, nullable=False)
    state_highway = db.Column(db.String(100), nullable=False)
    observation = db.Column(db.Text, nullable=True)
    verification_status = db.Column(db.String(100), nullable=True)
    verification_observation = db.Column(db.Text, nullable=True)

    def __init__(self, date, mission_id, highway_id, km_start, km_end, total_elements, state_highway,
                 observation, verification_status='', verification_observation=''):
        self.date = date
        self.mission_id = mission_id
        self.highway_id = highway_id
        self.km_start = km_start
        self.km_end = km_end
        self.extension = km_end - km_start
        self.total_elements = total_elements
        self.state_highway = state_highway
        self.observation = observation
        self.verification_status = verification_status
        self.verification_observation = verification_observation

    def to_dict(self):
        return {
            'id': self.id,
            'date': str(self.date),
            'mission': self.mission.to_dict() if self.mission_id else None,
            'highway': self.highway_obj.to_dict() if self.highway_obj else None,
            'km_start': self.km_start,
            'km_end': self.km_end,
            'extension': self.extension,
            'total_elements': self.total_elements,
            'state_highway': self.state_highway,
            'observation': self.observation,
            'verification_status': self.verification_status,
            'verification_observation': self.verification_observation
        }