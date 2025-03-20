from extensions import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    accounts = db.relationship('Account', secondary='account_permission', back_populates='permissions')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class AccountPermission(db.Model):
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)


    def __init__(self, account_id, permission_id):
        self.account_id = account_id
        self.permission_id = permission_id

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'permission_id': self.permission_id,
        }

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)

    permissions = db.relationship('Permission', secondary='account_permission', back_populates='accounts')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'permissions': [permission.to_dict() for permission in self.permissions]
        }

    def verification_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def validate_email(self):
        return True
