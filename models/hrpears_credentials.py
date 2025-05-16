#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Hrpears(db.Model):
    __tablename__ = 'hrpears_api'
    
    hrpears_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    hrpears_name = db.Column(db.String(200), nullable=False)
    hrpears_host = db.Column(db.String(200), nullable=False)
    hrpears_root = db.Column(db.String(200), nullable=False)
    hrpears_user = db.Column(db.String(200), nullable=False)
    hrpears_password = db.Column(db.String(200), nullable=False)
    hrpears_dbname = db.Column(db.String(200), nullable=False)
    hrpears_table = db.Column(db.String(255))
    
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def hrpears_data(self):
        return {
            'hrpears_id': self.hrpears_id,
            'hrpears_name': self.hrpears_name,
            'hrpears_host': self.hrpears_host,
            'hrpears_root': self.hrpears_root,
            'hrpears_user': self.hrpears_user,
            'hrpears_password': self.hrpears_password,
            'hrpears_dbname': self.hrpears_dbname,
            'hrpears_table': self.hrpears_table,
            
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
            
        }

    def get_id(self): 
        return str(self.hrpears_id)

    @staticmethod
    def get_all():
        return Hrpears.query.all()

    @staticmethod
    def get_by_id(hrpears_id):
        return Hrpears.query.get(hrpears_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>