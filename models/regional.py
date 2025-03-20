from extensions import db

class Highway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    km_start = db.Column(db.Float, nullable=False)
    km_end = db.Column(db.Float, nullable=False)
    extension = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(255), nullable=False)
    jurisdiction = db.Column(db.String(255), nullable=False)
    administration = db.Column(db.String(255), nullable=False)
    surface = db.Column(db.String(255), nullable=False)
    observation = db.Column(db.Text, nullable=True)
    regionais = db.relationship('Regional', secondary='regional_highway', back_populates='highways')

    def __init__(self, name, type, km_start, km_end, city, jurisdiction, administration, surface, observation):
        self.name = name
        self.type = type
        self.km_start = km_start
        self.km_end = km_end
        self.extension = km_end - km_start
        self.city = city
        self.jurisdiction = jurisdiction
        self.administration = administration
        self.surface = surface
        self.observation = observation


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'km_start': self.km_start,
            'km_end': self.km_end,
            'extension': self.extension,
            'city': self.city,
            'jurisdiction': self.jurisdiction,
            'administration': self.administration,
            'surface': self.surface,
            'observation': self.observation
        }

class RegionalHighway(db.Model):
    regional_id = db.Column(db.Integer, db.ForeignKey('regional.id'), primary_key=True)
    highway_id = db.Column(db.Integer, db.ForeignKey('highway.id'), primary_key=True)

class Regional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    observation = db.Column(db.Text)
    km_start = db.Column(db.Float, nullable=False)
    km_end = db.Column(db.Float, nullable=False)
    highways = db.relationship('Highway', secondary='regional_highway', back_populates='regionais')

    def __init__(self, name, observation, km_start, km_end):
        self.name = name
        self.observation = observation
        self.km_start = km_start
        self.km_end = km_end

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'observation': self.observation,
            'km_start': self.km_start,
            'km_end': self.km_end,
            'highways': [highway.to_dict() for highway in self.highways]
        }