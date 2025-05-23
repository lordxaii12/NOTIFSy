#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from models.user_role import Roles
from models.user_themes import Theme

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class User_v1(db.Model, UserMixin):
    __tablename__ = 'userv1'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.String(200), unique=True, nullable=False)
    full_name = db.Column(db.String(200), unique=True, nullable=False)
    user_email = db.Column(db.String(200), unique=False, nullable=True)
    division = db.Column(db.String(50), unique=False, nullable=True)
    user_section = db.Column(db.String(255), unique=False, nullable=True)
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.theme_id'), nullable=True)
    
    login_status = db.Column(db.String(50), unique=False, nullable=True)
    login_error_counter = db.Column(db.String(50), unique=False, nullable=True)
    
    cur_login = db.Column(db.String(100), unique=False, nullable=True)
    last_login = db.Column(db.String(100), unique=False, nullable=True)
    last_logout = db.Column(db.String(100), unique=False, nullable=True)
    user_notes = db.Column(db.Text, unique=False, nullable=True)
    
    msg_sent = db.Column(db.Integer, unique=False, nullable=True)
    credit_used = db.Column(db.Integer, unique=False, nullable=True)
    
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
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
            'user_email': self.user_email,
            'division': self.division,
            'user_section': self.user_section,
            
            'role_id': self.role_id,
            'role_name': self.role.role_name if self.role else None,
            'theme_id': self.theme_id,
            'theme_name': self.theme.theme_name if self.theme else None,
            
            'login_status': self.login_status,
            'login_error_counter': self.login_error_counter,
            
            'cur_login': self.cur_login,
            'last_login': self.last_login,
            'last_logout': self.last_logout,
            'user_notes': self.user_notes,
            'msg_sent': self.msg_sent,
            'credit_used': self.credit_used,
            
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
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

#===============================================================================================================================>
