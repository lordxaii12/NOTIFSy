from models.msg_log import Msg_log
from extensions import db
from flask import request,flash
from flask_login import current_user
from utils import get_manila_time

def add_msg_log(msg_tracker, msg_type, msg_recipient, msg_content, msg_status):
    
    msg_sender = current_user.full_name
    sent_on = get_manila_time()

    new_msg = Msg_log(
        msg_tracker=msg_tracker,
        msg_type=msg_type,
        msg_recipient=msg_recipient,
        msg_content=msg_content,
        msg_status=msg_status,
        msg_sender=msg_sender,
        sent_on=sent_on
    )
    try:
        db.session.add(new_msg)
        db.session.commit()
        return new_msg 
    except Exception as e:
        db.session.rollback()
        return None 


def delete_msg_log(msg_id):
    
    msg = Msg_log.get_by_id(msg_id)
    if not msg:
        return False 
    try:
        db.session.delete(msg)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


# def send_single_msg():
    