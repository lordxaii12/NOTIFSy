from models.msg_log import Msg_log
from extensions import db
import requests
from flask_login import current_user
from utils import get_manila_time
from flask import g, flash
from models.email_credentials import Ecredss
from models.itexmo_credentials import Itexmo


def add_msg_log(msg_tracker, msg_type, msg_recipient, msg_content, msg_status, msg_sent, msg_unsent, credit_used):
    
    msg_sender = current_user.full_name
    sent_on = get_manila_time()

    new_msg = Msg_log(
        msg_tracker=msg_tracker,
        msg_type=msg_type,
        msg_recipient=msg_recipient,
        msg_content=msg_content,
        msg_status=msg_status,
        
        msg_sender=msg_sender,
        sent_on=sent_on,
        
        msg_sent=msg_sent,
        msg_unsent=msg_unsent,
        credit_used=credit_used
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

def send_msg(message, recipient):
    sms_id = g.sys_settings.msg_api_id if g.sys_settings and g.sys_settings.msg_api_id else 1
    sms_data = Itexmo.get_by_id(sms_id)
    
    if sms_data:
        url = sms_data.itexmo_url
        email = sms_data.itexmo_email
        password = sms_data.itexmo_password
        apicode = sms_data.itexmo_apicode
        content_type = sms_data.itexmo_contenttype
        
        payload = {
            "Email": email,
            "Password": password,
            "ApiCode": apicode,
            "Message": message,
            "Recipients": [recipient]
        }
        headers = {
            "Content-Type": content_type
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return (response.status_code, response.json())

    else:
        flash('PLEASE CHECK SMS API CREDENTIALS.', 'error')



# status, data = send_msg("Hello", ["09263302179"])
# print("Status Code:", status)
# print("Response Data:", data)