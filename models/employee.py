from extensions import db
from models.branch import Branch
from models.department import Department
from models.position import Position

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_of_hire = db.Column(db.Date, nullable=True)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    phone = db.Column(db.String(13), nullable=True)
    phone_contact = db.Column(db.String(13), nullable=True)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, unique=True)
    account = db.relationship('Account')
    id_branch = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    branch = db.relationship('Branch')
    id_department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    department = db.relationship('Department')
    id_position = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    position = db.relationship('Position')
    gender = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    blood_type = db.Column(db.String(255), nullable=True)
    medical_condition = db.Column(db.String(255), nullable=True)
    allergy = db.Column(db.String(255), nullable=True)
    regular_medication = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)

    def __init__(self, name, date_of_birth, cpf, id_account, id_branch, id_department, id_position, address, date_of_hire,
                 phone=None, phone_contact=None, gender=None, blood_type=None, medical_condition=None,
                 allergy=None, regular_medication=None, active=True):
        self.name = name
        self.date_of_birth = date_of_birth
        self.cpf = cpf
        self.phone = phone
        self.phone_contact = phone_contact
        self.id_account = id_account
        self.id_branch = id_branch
        self.id_department = id_department
        self.id_position = id_position
        self.gender = gender
        self.address = address
        self.blood_type = blood_type
        self.medical_condition = medical_condition
        self.allergy = allergy
        self.regular_medication = regular_medication
        self.active = active
        self.date_of_hire = date_of_hire

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None,
            "cpf": self.cpf,
            "phone": self.phone,
            "phone_contact": self.phone_contact,
            "account": self.account.to_dict() if self.account else None,
            "branch": self.branch.to_dict() if self.branch else None,
            "department": self.department.to_dict() if self.department else None,
            "position": self.position.to_dict() if self.position else None,
            "gender": self.gender,
            "address": self.address,
            "blood_type": self.blood_type,
            "medical_condition": self.medical_condition,
            "allergy": self.allergy,
            "regular_medication": self.regular_medication,
            "active": self.active,
            "date_of_hire": self.date_of_hire
        }
