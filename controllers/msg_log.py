#--CODE BY: RYRUBIO--#
#===============================================================================================================================>
from models.msg_log import Msg_log
from extensions import db, cache
import requests
from flask_login import current_user
from utils import get_manila_time
from flask import g, flash
from models.email_credentials import Ecredss
from models.itexmo_credentials import Itexmo
import json
from models.hrpears_credentials import Hrpears
import pymysql

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
#
#================ SEND MESSAGE =================================================================================================>
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

#===============================================================================================================================>
#
#================ FETCH DATE FROM HRIS =========================================================================================>
@cache.cached(timeout=300)
def get_table_data():
    hris_id = g.sys_settings.hris_api_id if g.sys_settings and g.sys_settings.hris_api_id else 1
    hris_data = Hrpears.get_by_id(hris_id)
    
    DB_HOST = hris_data.hrpears_host
    DB_USER = hris_data.hrpears_user
    DB_PASSWORD = hris_data.hrpears_password
    DB_NAME = hris_data.hrpears_dbname
    DB_TABLE = hris_data.hrpears_table

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:

            query = f"SELECT first_name, last_name, middle_name, email, mobile_no FROM {DB_TABLE}"
            cursor.execute(query)
            data = cursor.fetchall()
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
    return data

#===============================================================================================================================>
