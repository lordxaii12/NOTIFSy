#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Itexmo(db.Model):
    __tablename__ = 'itexmo_api'
    
    itexmo_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    itexmo_name = db.Column(db.String(200), nullable=False)
    itexmo_url = db.Column(db.String(200), nullable=False)
    itexmo_email = db.Column(db.String(200), nullable=False)
    itexmo_password = db.Column(db.String(200), nullable=False)
    itexmo_apicode = db.Column(db.String(200), nullable=False)
    itexmo_contenttype = db.Column(db.String(255))
    
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    credits_remaining = db.Column(db.Integer, unique=False, nullable=True)
    credits_consumed = db.Column(db.Integer, unique=False, nullable=True)

    @property
    def itexmo_data(self):
        return {
            'itexmo_id': self.itexmo_id,
            'itexmo_name': self.itexmo_name,
            'itexmo_url': self.itexmo_url,
            'itexmo_email': self.itexmo_email,
            'itexmo_password': self.itexmo_password,
            'itexmo_apicode': self.itexmo_apicode,
            'itexmo_contenttype': self.itexmo_contenttype,
            
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on,
            'credits_remaining': self.credits_remaining,
            'credits_consumed': self.credits_consumed
            
        }

    def get_id(self): 
        return str(self.itexmo_id)

    @staticmethod
    def get_all():
        return Itexmo.query.all()

    @staticmethod
    def get_by_id(itexmo_id):
        return Itexmo.query.get(itexmo_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>