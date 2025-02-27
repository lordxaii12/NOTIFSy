#--CODE BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Divisions(db.Model):
    __tablename__ = 'divisions'
    
    division_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    division_name = db.Column(db.String(100), nullable=False)
    division_description = db.Column(db.String(255))
    created_by = db.Column(db.String(100), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(100), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def divisions_data(self):
        return {
            'division_id': self.division_id,
            'division_name': self.division_name,
            'division_description': self.division_description,
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.division_id)

    @staticmethod
    def get_all():
        return Divisions.query.all()

    @staticmethod
    def get_by_id(division_id):
        return Divisions.query.get(division_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>