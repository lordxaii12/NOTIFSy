#--CODE BY: RYRUBIO--#
#===============================================================================================================================>
from extensions import db
from sqlalchemy.sql import func

#===============================================================================================================================>
#
#================ CLASS ========================================================================================================>
class Theme(db.Model):
    __tablename__ = 'theme'
    
    theme_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    theme_name = db.Column(db.String(100),unique=False, nullable=True)
    
    theme_bg = db.Column(db.String(100),unique=False, nullable=True)
    theme_font = db.Column(db.String(100),unique=False, nullable=True)
    theme_icon = db.Column(db.String(100),unique=False, nullable=True)
    
    theme_description = db.Column(db.String(255))
    
    created_by = db.Column(db.String(100), unique=False, nullable=True)
    created_on = db.Column(db.String(100), unique=False, nullable=True)
    
    updated_by = db.Column(db.String(100), unique=False, nullable=True)
    updated_on = db.Column(db.String(100), unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def themes_data(self):
        return {
            'theme_id': self.theme_id,
            'theme_name': self.theme_name,
            
            'theme_bg': self.theme_bg,
            'theme_font': self.theme_font,
            'theme_icon': self.theme_icon,
            
            'theme_description': self.theme_description,
            
            'created_by': self.created_by,
            'created_on': self.created_on,
            'updated_by': self.updated_by,
            'updated_on': self.updated_on
        }

    def get_id(self): 
        return str(self.theme_id)

    @staticmethod
    def get_all():
        return Theme.query.all()

    @staticmethod
    def get_by_id(theme_id):
        return Theme.query.get(theme_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#===============================================================================================================================>