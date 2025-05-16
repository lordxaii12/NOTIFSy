#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class External(db.Model):
    __tablename__ = 'external_contacts'

    external_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    external_name = db.Column(db.String(100), nullable=False)
    external_mobile = db.Column(db.String(100), nullable=False)
    external_email = db.Column(db.String(100), nullable=False)
    external_description = db.Column(db.String(255))
    
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def externals_data(self):
        return {
            'external_id': self.external_id,
            'external_name': self.external_name,
            'external_mobile': self.external_mobile,
            'external_email': self.external_email,
            'external_description': self.external_description,
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.external_id)

    @staticmethod
    def get_all():
        return External.query.all()

    @staticmethod
    def get_by_id(external_id):
        return External.query.get(external_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>