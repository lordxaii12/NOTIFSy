#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func
from models.itexmo_credentials import Itexmo
from models.email_credentials import Ecredss
from models.hrpears_credentials import Hrpears
from models.login_credentials import LogApi

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class SysSettings(db.Model):
    __tablename__ = 'sys_setting'
    
    sys_setting_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    sys_name = db.Column(db.String(200),unique=True, nullable=False)
    sys_app_name = db.Column(db.String(200),unique=True, nullable=True)
    sys_app_user = db.Column(db.String(100),unique=False, nullable=True)
    sys_app_email = db.Column(db.String(100),unique=False, nullable=True)
    sys_app_phone = db.Column(db.String(100),unique=False, nullable=True)
    
    sys_app_user_text = db.Column(db.String(900),unique=False, nullable=True)
    sys_app_role_text = db.Column(db.String(900),unique=False, nullable=True)
    sys_app_division_text = db.Column(db.String(900),unique=False, nullable=True)
    sys_app_logs_text = db.Column(db.String(900),unique=False, nullable=True)
    
    sys_app_itexmo_credits_url = db.Column(db.String(900),unique=False, nullable=True)
    sys_app_eprocsys_supplier_url = db.Column(db.String(900),unique=False, nullable=True)
    
    msg_api_id = db.Column(db.Integer, db.ForeignKey('itexmo_api.itexmo_id'), nullable=True)
    email_api_id = db.Column(db.Integer, db.ForeignKey('email_api.ecreds_id'), nullable=True)
    hris_api_id = db.Column(db.Integer, db.ForeignKey('hrpears_api.hrpears_id'), nullable=True)
    login_api_id = db.Column(db.Integer, db.ForeignKey('login_api.login_api_id'), nullable=True)
    
    created_by = db.Column(db.String(200), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    updated_by = db.Column(db.String(200), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
        
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    msg_api = db.relationship('Itexmo', backref='sys_settings')
    email_api = db.relationship('Ecredss', backref='sys_settings')
    hris_api = db.relationship('Hrpears', backref='sys_settings')
    login_api = db.relationship('LogApi', backref='sys_settings')
    
    system_notice = db.Column(db.Text, unique=False, nullable=True)

    @property
    def sys_settings_data(self):
        return {
            'sys_setting_id': self.sys_setting_id,
            'sys_name': self.sys_name,
            'sys_app_name': self.sys_app_name,
            'sys_app_user': self.sys_app_user,
            'sys_app_email': self.sys_app_email,
            'sys_app_phone': self.sys_app_phone,
            
            'sys_app_user_text': self.sys_app_user_text,
            'sys_app_role_text': self.sys_app_role_text,
            'sys_app_division_text': self.sys_app_division_text,
            'sys_app_logs_text': self.sys_app_logs_text,

            'msg_api_id': self.msg_api_id,
            'itexmo_name': self.msg_api.itexmo_name if self.msg_api else None,
            'email_api_id': self.email_api_id,
            'ecreds_email': self.email_api.ecreds_email if self.email_api else None,
            'hris_api_id': self.hris_api_id,
            'hrpears_name': self.hris_api.hrpears_name if self.hris_api else None,
            'login_api_id': self.login_api_id,
            'login_api_name': self.login_api.login_api_name if self.login_api else None,
            
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on,
            
            'system_notice': self.system_notice
        }

    def get_id(self): 
        return str(self.sys_setting_id)

    @staticmethod
    def get_all():
        return SysSettings.query.all()

    @staticmethod
    def get_by_id(sys_setting_id):
        return SysSettings.query.get(sys_setting_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>