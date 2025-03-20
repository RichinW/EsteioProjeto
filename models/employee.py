from extensions import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    phone = db.Column(db.String(13), nullable=True)
    phone_contact = db.Column(db.String(13), nullable=True)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, unique=True)
    account = db.relationship('Account')

    def __init__(self, name, date_of_birth, cpf, phone, phone_contact, id_account):
        self.name = name,
        self.date_of_birth = date_of_birth,
        self.cpf = cpf,
        self.phone = phone,
        self.phone_contact = phone_contact,
        self.id_account = id_account

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_of_birth': str(self.date_of_birth),
            'cpf': self.cpf,
            'phone': self.phone,
            'phone_contact': self.phone_contact,
            'account': self.account.to_dict() if self.id_account else None
        }
