from extensions import db
from sqlalchemy import Enum
from models.enums import StatusVerification
from models.team import Team

class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    audit = db.Column(db.Integer, nullable=False)

    team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team_obj = db.relationship('Team')

    highway = db.Column(db.String(100), nullable=False)
    km_start = db.Column(db.Float, nullable=False)
    km_end = db.Column(db.Float, nullable=False)
    extension = db.Column(db.Float, nullable=False)
    total_elements = db.Column(db.Integer, nullable=False)
    state_highway = db.Column(db.String(100), nullable=False)
    observation = db.Column(db.Text, nullable=True)
    verification_status = db.Column(Enum(StatusVerification), nullable=True)
    verification_observation = db.Column(db.Text, nullable=True)

    def __init__(self, date, type, activity, audit, team, highway, km_start, km_end, total_elements, state_highway,
                 observation, verification_status, verification_observation):
        self.date = date
        self.type = type
        self.activity = activity
        self.audit = audit
        self.team = team
        self.highway = highway
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
            'type': self.type,
            'activity': self.activity,
            'audit': self.audit,
            'team': self.team_obj.to_dict() if self.team else None,
            'highway': self.highway,
            'km_start': self.km_start,
            'km_end': self.km_end,
            'extension': self.extension,
            'total_elements': self.total_elements,
            'state_highway': self.state_highway,
            'observation': self.observation,
            'verification_status': self.verification_status,
            'verification_observation': self.verification_observation
        }