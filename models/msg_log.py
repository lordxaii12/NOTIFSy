from extensions import db
from sqlalchemy.sql import func


class Msg_log(db.Model):
    __tablename__ = 'msg_log'
    
    msg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    msg_tracker = db.Column(db.String(50), unique=True, nullable=False)
    msg_type = db.Column(db.String(50), unique=False, nullable=False)
    msg_sender = db.Column(db.String(50), unique=False, nullable=False)
    msg_recipient = db.Column(db.Text, unique=False, nullable=True)
    msg_content = db.Column(db.Text, unique=False, nullable=True)
    msg_status = db.Column(db.String(50), unique=False, nullable=True)
    sent_on = db.Column(db.String(100), unique=False, nullable=True)
    
    msg_sent = db.Column(db.Text, unique=False, nullable=True)
    msg_unsent = db.Column(db.Text, unique=False, nullable=True)
    credit_used = db.Column(db.Integer, unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    @property
    def user_data(self):
        return {
            'msg_id': self.msg_id,
            'msg_tracker': self.msg_tracker,
            
            'msg_type': self.msg_type,
            'msg_sender': self.msg_sender,
            
            'msg_recipient': self.msg_recipient,
            'msg_content': self.msg_content,
            
            'msg_status': self.msg_status,
            'sent_on': self.sent_on,
            
            'msg_sent': self.msg_sent,
            'msg_unsent': self.msg_unsent,
            'credit_used': self.credit_used
        }

    def get_id(self):
        return str(self.msg_id)

    @staticmethod
    def get_all():
        return Msg_log.query.order_by(Msg_log.created_at.desc()).all()

    @staticmethod
    def get_by_id(msg_id):
        return Msg_log.query.get(msg_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
