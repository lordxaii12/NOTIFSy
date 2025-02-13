from extensions import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from models.role import Roles
from models.themes import Theme

class User_v1(db.Model, UserMixin):
    __tablename__ = 'userv1'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    division = db.Column(db.String(50), unique=False, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.theme_id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    role = db.relationship('Roles', backref='users')
    theme = db.relationship('Theme', backref='users')

    @property
    def user_data(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'division': self.division,
            'role_id': self.role_id,
            'role_name': self.role.role_name if self.role else None,
            'theme_id': self.theme_id,
            'theme_name': self.theme.theme_name if self.theme else None
        }

    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def get_all():
        return User_v1.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User_v1.query.get(user_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
