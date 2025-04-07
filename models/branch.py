from extensions import db

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, name, address):
        self.name = name,
        self.address = address,


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

