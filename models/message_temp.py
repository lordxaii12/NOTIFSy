#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Msg_templates(db.Model):
    __tablename__ = 'msg_templates'
    
    msg_temp_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    msg_temp_name = db.Column(db.String(100), nullable=False)
    msg_temp_description = db.Column(db.String(255))
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def msg_temps_data(self):
        return {
            'msg_temp_id': self.msg_temp_id,
            'msg_temp_name': self.msg_temp_name,
            'msg_temp_description': self.msg_temp_description,
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.msg_temp_id)

    @staticmethod
    def get_all():
        return Msg_templates.query.all()

    @staticmethod
    def get_by_id(msg_temp_id):
        return Msg_templates.query.get(msg_temp_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>