from extensions import db

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regional = db.Column(db.String(255), nullable=False)
    km_start = db.Column(db.Float, nullable=False)
    km_end = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=True)

    def __init__(self, km_start, km_end, duration, active=True):

        self.km_start = km_start
        self.km_end = km_end
        self.duration = duration
        self.active = active

    def to_dict(self):
        return {
            'id': self.id,
            'regional': self.regional,
            'km_start': self.km_start,
            'km_end': self.km_end,
            'duration': str(self.duration),
            'active': self.active
        }
