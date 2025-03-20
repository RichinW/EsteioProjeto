from extensions import db
from models.regional import Regional
from models.team import Team

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    observation = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    audit = db.Column(db.Integer, nullable=False)
    regional_id = db.Column(db.Integer, db.ForeignKey('regional.id'), nullable=False)
    regional = db.relationship('Regional', backref='missions', lazy=True)
    km_start = db.Column(db.Float, nullable=False)
    km_end = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team')


    def __init__(self, name, observation, type, activity, audit, regional_id, km_start, km_end, start_date, end_date, team_id, active=True ):
        self.name = name
        self.observation = observation
        self.type = type
        self.activity = activity
        self.audit = audit
        self.regional_id = regional_id
        self.km_start = km_start
        self.km_end = km_end
        self.start_date = start_date
        self.end_date = end_date
        self.active = active
        self.team_id = team_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'observation': self.observation,
            'type': self.type,
            'activity': self.activity,
            'audit': self.audit,
            'regional': self.regional.to_dict() if self.regional else None,
            'km_start': self.km_start,
            'km_end': self.km_end,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'active': self.active,
            'team': self.team.to_dict() if self.team_id else None
        }
