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
import re

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

def format_mobile_number(mobile_no):
    if not mobile_no:
        return "Not Found"
    mobile_no = mobile_no.strip()
    if mobile_no.startswith("+63"):
        mobile_no = "0" + mobile_no[3:]
    if not mobile_no.startswith("0"):
        mobile_no = "0" + mobile_no
    if mobile_no == "0" * 11:
        return "Not Found"
    return mobile_no if len(mobile_no) == 11 and mobile_no.isdigit() else "Not Found"

def format_email(email):
    if not email:
        return "Not Found"
    email = email.strip()
    if "@" not in email:
        return "Not Found"
    if not email.endswith(".com"):
        email += ".com"
    if email.startswith("default"):
        return "Not Found"
    return email if re.match(r"[^@]+@[^@]+\.[a-zA-Z]{2,}", email) else "Not Found"

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
            raw_data = cursor.fetchall()
            formatted_data = []
            for row in raw_data:
                last_name = row["last_name"].upper() if row["last_name"] else ""
                first_name = row["first_name"].upper() if row["first_name"] else ""
                middle_name = row["middle_name"].upper() if row["middle_name"] else ""
                formatted_name = f"{last_name}, {first_name} {middle_name}".strip()
                formatted_mobile = format_mobile_number(row["mobile_no"])
                formatted_email = format_email(row["email"])
                formatted_data.append({
                    "name": formatted_name,
                    "email": formatted_email,
                    "mobile_no": formatted_mobile
                })
            return formatted_data

    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

#===============================================================================================================================>
