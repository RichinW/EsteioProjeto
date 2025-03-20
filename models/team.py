from extensions import db
from sqlalchemy.sql import func

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_employee_one = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    id_employee_two = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date_register = db.Column(db.Date, default=func.current_date(), nullable=False)
    employee_one = db.relationship('Employee', foreign_keys=[id_employee_one])
    employee_two = db.relationship('Employee', foreign_keys=[id_employee_two])

    def __init__(self, id_employee_one, id_employee_two):
        self.id_employee_one = id_employee_one
        self.id_employee_two = id_employee_two

    def to_dict(self):
        return {
            'id': self.id,
            'employee_one': self.employee_one.to_dict(),
            'employee_two': self.employee_two.to_dict(),
            'date_register': self.date_register
        }

