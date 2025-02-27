#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Ecredss(db.Model):
    __tablename__ = 'email_api'
    
    ecreds_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    ecreds_name = db.Column(db.String(100), unique=True, nullable=False)
    ecreds_email = db.Column(db.String(100), unique=True, nullable=False)
    ecreds_sender = db.Column(db.String(100), nullable=True)
    ecreds_password = db.Column(db.String(100), nullable=False)
    
    created_by = db.Column(db.String(100), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(100), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def ecredss_data(self):
        return {
            'ecreds_id': self.ecreds_id,
            'ecreds_name': self.ecreds_name,
            'ecreds_email': self.ecreds_email,
            'ecreds_sender': self.ecreds_sender,
            'ecreds_password': self.ecreds_password,
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.ecreds_id)

    @staticmethod
    def get_all():
        return Ecredss.query.all()

    @staticmethod
    def get_by_id(ecreds_id):
        return Ecredss.query.get(ecreds_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>