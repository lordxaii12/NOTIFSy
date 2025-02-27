#--CODE BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class LogApi(db.Model):
    __tablename__ = 'login_api'
    
    login_api_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    login_api_name = db.Column(db.String(100),unique=True, nullable=False)
    login_api_url = db.Column(db.String(100), nullable=False)
    login_api_token = db.Column(db.String(200), nullable=False)
    login_api_content_type = db.Column(db.String(100), nullable=False)
    
    created_by = db.Column(db.String(100), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(100), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def roles_data(self):
        return {
            'login_api_id': self.login_api_id,
            'login_api_name': self.login_api_name,
            'login_api_url': self.login_api_url,
            'login_api_token': self.login_api_token,
            'login_api_content_type': self.login_api_content_type,
            
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.login_api_id)

    @staticmethod
    def get_all():
        return LogApi.query.all()

    @staticmethod
    def get_by_id(login_api_id):
        return LogApi.query.get(login_api_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>