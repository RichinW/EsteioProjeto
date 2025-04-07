from extensions import db


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, name, description=None):
        self.name = name,
        self.name = description


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

