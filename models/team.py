from extensions import db
from models.mission import Mission

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_employee_one = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    id_employee_two = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    id_mission = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    mission = db.relationship('Mission')
    employee_one = db.relationship('Employee', foreign_keys=[id_employee_one])
    employee_two = db.relationship('Employee', foreign_keys=[id_employee_two])

    def __init__(self, id_employee_one, id_employee_two, id_mission):

        self.id_employee_one = id_employee_one
        self.id_employee_two = id_employee_two
        self.id_mission = id_mission

    def to_dict(self):
        return {
            'id': self.id,
            'employee_one': self.employee_one.to_dict(),
            'employee_two': self.employee_two.to_dict(),
            'id_mission': self.mission.to_dict() if self.id_mission else None
        }

