#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Roles(db.Model):
    __tablename__ = 'roles'
    
    role_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), nullable=False)
    role_description = db.Column(db.String(255))
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def roles_data(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_description': self.role_description,
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.role_id)

    @staticmethod
    def get_all():
        return Roles.query.all()

    @staticmethod
    def get_by_id(role_id):
        return Roles.query.get(role_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>