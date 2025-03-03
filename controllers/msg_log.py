#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.msg_log import Msg_log
from extensions import db
from flask_login import current_user
import json

from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_msg_log(msg_tracker, msg_type, msg_recipient, msg_content, msg_status, msg_sent, msg_unsent, credit_used):
    
    msg_sender = current_user.full_name
    sent_on = get_manila_time()
    
    msg_sent_str = json.dumps(msg_sent) if isinstance(msg_sent, list) else msg_sent
    msg_unsent_str = json.dumps(msg_unsent) if isinstance(msg_unsent, list) else msg_unsent

    new_msg = Msg_log(
        msg_tracker=msg_tracker,
        msg_type=msg_type,
        msg_recipient=msg_recipient,
        msg_content=msg_content,
        msg_status=msg_status,
        
        msg_sender=msg_sender,
        sent_on=sent_on,
        
        msg_sent=msg_sent_str,
        msg_unsent=msg_unsent_str,
        
        credit_used=credit_used
    )
    try:
        db.session.add(new_msg)
        db.session.commit()
        return new_msg 
    except Exception as e:
        db.session.rollback()
        print(f"Error saving message log: {str(e)}")
        return None 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>   
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

#===============================================================================================================================>
