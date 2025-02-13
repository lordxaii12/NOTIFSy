from extensions import db
from sqlalchemy.sql import func

class User_logs(db.Model):
    __tablename__ = 'user_logs'
    
    log_id = db.Column(db.Integer,unique=True, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50), unique=True, nullable=False)
    activity = db.Column(db.String(999), unique=True, nullable=False)
    created_on = db.Column(db.String(100), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def log_data(self):
        return {
            'log_id': self.log_id,
            'user': self.user,
            'activity': self.activity,
            'created_on': self.created_on
        }

    def get_id(self):  # Fixed method
        return str(self.log_id)

    @staticmethod
    def get_all():
        return User_logs.query.all()

    @staticmethod
    def get_by_id(log_id):
        return User_logs.query.get(log_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
