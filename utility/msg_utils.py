#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
import random
import re
import pymysql
from flask import g
from extensions import db, cache
from models.itexmo_credentials import Itexmo
from models.hrpears_credentials import Hrpears
import requests
from models.itexmo_credentials import Itexmo
from controllers.itexmo_credentials import credits_check
from utility.format_utils import extract_first_name, format_mobile_number, format_email
import requests

#===============================================================================================================================>
    #Track API IP address
def get_my_ip_used_to_reach(url=None):
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
#===============================================================================================================================>
    #Generate Msg send tracking number
def generate_tracker(sender_div, msg_type):
    random_number = random.randint(1, 9999)
    tracking_number = f"{sender_div}-{msg_type}:{random_number}"
    return tracking_number
#===============================================================================================================================>
    #Format message for including/excluding name
def message_content(add_name,recipient_name,msg_content,sender,sender_div):
    if add_name == 'on':
        message = f"Hi {recipient_name}, {msg_content}\n\n{sender}\n{sender_div}"
    else:
        message = f"Hi, {msg_content}\n\n{sender}\n{sender_div}"
    return message
#===============================================================================================================================>
    #Format message for including/excluding name
def message_content2(add_name,recipient_name,amount,msg_content,sender,sender_div):
    
    if add_name == 'on':
        message = f"Hi {recipient_name}, an amount of {amount} as {msg_content}\n\n{sender}\n{sender_div}"
    else:
        message = f"Hi, an amount of {amount} {msg_content}\n\n{sender}\n{sender_div}"
    return message

#===============================================================================================================================>
    #Create status data for message logs status
def get_status_data(recipient_name,recipient_contact,message):
    status_data = f"{recipient_name}:{recipient_contact}:{message}"
    return status_data
#===============================================================================================================================>
    #Display HR data to directory
@cache.cached(timeout=300)
def get_hrpears_data():
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
    #Send sms 
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
        
        public_ip = get_my_ip_used_to_reach()
        print(f"[LOG] Public IP used for API call: {public_ip}")
        
        return (url,payload,headers)
#===============================================================================================================================>
    #Upload file and search in hr data
def convert_file_to_inputs(file):
    if file is None:
        print("No file received in function")
        return [], []

    try:
        content = file.stream.read().decode("utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], []

    file.stream.seek(0) 
    
    hris_id = g.sys_settings.hris_api_id if g.sys_settings and g.sys_settings.hris_api_id else 1
    hris_data = Hrpears.get_by_id(hris_id)
    DB_HOST = hris_data.hrpears_host
    DB_USER = hris_data.hrpears_user
    DB_PASSWORD = hris_data.hrpears_password
    DB_NAME = hris_data.hrpears_dbname
    DB_TABLE = hris_data.hrpears_table

    data_list = []
    name_list = []
    raw_names = []
    amount_list = []

    for line in content.splitlines():
            account_number = line[:10].strip()
            account_name = line[10:50].strip().lower()
            raw_names.append(account_name)

            name_search = account_name.replace(" ", "").replace(",", "").replace(".", "").lower()

            amount_raw = line[51:65].strip().lstrip("0")
            amount = f"{int(amount_raw) / 100:.2f}" if amount_raw else "0.00"

            if account_number == "9999999999":
                break

            data_list.append(account_number)
            name_list.append(name_search)
            amount_list.append(amount)
            

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    matched_records = []
    matched_names = set()
    not_found_list = []
    try:
        with connection.cursor() as cursor:
            query = f"SELECT first_name, last_name, middle_name, email, mobile_no, account_number FROM {DB_TABLE}"
            cursor.execute(query)
            raw_data = cursor.fetchall()

            for row in raw_data:
                db_fn = row["first_name"] if row["first_name"] else ""
                db_mn = row["middle_name"] if row["middle_name"] else ""
                db_ln = row["last_name"] if row["last_name"] else ""

                format_name = f"{db_ln} {db_fn} {db_mn}".strip().lower()
                db_format_name = format_name.replace(" ", "").replace(",", "").replace(".", "")

                for i, file_name in enumerate(name_list):
                    if db_format_name in file_name or file_name in db_format_name:
                        matched_names.add(file_name)

                        first_name = row["first_name"] if row["first_name"] else ""
                        middle_name = row["middle_name"] if row["middle_name"] else ""
                        last_name = row["last_name"] if row["last_name"] else ""
                        fullname = f"{last_name}, {first_name} {middle_name}".strip()

                        matched_records.append({
                            "account_number": row["account_number"],
                            "fullname": fullname.upper(),
                            "first_name": extract_first_name(fullname),
                            "mobile": format_mobile_number(row["mobile_no"]),
                            "email": format_email(row["email"]),
                            "amount": amount_list[i]
                        })

            for i, name in enumerate(name_list):
                if name not in matched_names:
                    not_found_details = f"{raw_names[i].upper()}:-> {amount_list[i]}"
                    not_found_list.append(not_found_details)

    finally:
        connection.close()

    return matched_records, not_found_list 
#===============================================================================================================================>
    #Upload file and search in hr data
def sms_API_credits_checker():
    sms_id = g.sys_settings.msg_api_id if g.sys_settings and g.sys_settings.msg_api_id else 1
    api_data = Itexmo.get_by_id(sms_id)
    credit_checker = g.sys_settings.sys_app_itexmo_credits_url
    if api_data:
        url = credit_checker
        email = api_data.itexmo_email
        password = api_data.itexmo_password
        apicode = api_data.itexmo_apicode
        action = "ApiCodeInfo"
        content_type = api_data.itexmo_contenttype
        payload = {
            "Email": email,
            "Password": password,
            "ApiCode": apicode,
            "Action": action
        }
        headers = {
            "Content-Type": content_type
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        messages_left = int(data.get("MessagesLeft", 0))
        total_credit_used = int(data.get("TotalCreditUsed", 0))
        
        credits_check(sms_id,messages_left,total_credit_used)
#===============================================================================================================================>
    #Display supplier data to directory
@cache.cached(timeout=300)
def get_eprocsys_data():
    api_url = g.sys_settings.sys_app_eprocsys_supplier_url
    try:
        # Send GET request
        response = requests.get(api_url)
        response.raise_for_status()

        # Parse JSON response
        data = response.json()
        
        # Process data
        extracted_data = []
        for item in data:
            payee_name = item.get('PayeeName', '').strip().upper()
            mobile = format_mobile_number(item.get('Mobile', ''))
            email = format_email(item.get('Email', ''))

            extracted_data.append({
                "name": payee_name,
                "email": email,
                "mobile_no": mobile
            })
        return extracted_data
    except requests.exceptions.RequestException as e:
        return []
    except ValueError:
        return []
#===============================================================================================================================>