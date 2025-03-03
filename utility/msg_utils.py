#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
import random
import re
import pymysql
from flask import g
from extensions import db, cache
from models.itexmo_credentials import Itexmo
from models.hrpears_credentials import Hrpears

#===============================================================================================================================>
    #Generate Msg send tracking number
def generate_tracker(sender_div, msg_type):
    random_number = random.randint(1, 9999)
    tracking_number = f"{sender_div}-{msg_type}:{random_number}"
    return tracking_number

#===============================================================================================================================>
    #Extract first name from fullname
def extract_first_name(full_name):
    parts = full_name.split(",", 1)
    if len(parts) < 2:
        return "Not Found"
    first_middle = parts[1].strip().split()
    prefixes = {"MA.", "JR.", "SR.", "II", "III"}
    for word in first_middle:
        if word not in prefixes:
            return word
    return "Not Found"

#===============================================================================================================================>
    #Format mobile number to 09xxxxxxxxx
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
    if mobile_no.startswith("090000"): 
        return "Not Found"
    
    return mobile_no if len(mobile_no) == 11 and mobile_no.isdigit() else "Not Found"

#===============================================================================================================================>
    #Format email with '@' and '.com'
def format_email(email):
    if not email:
        return "Not Found"
    email = email.strip()
    if "@" not in email:
        return "Not Found"
    if "dswd.gov.ph" not in email and not email.endswith(".com"):
        email += ".com"
    if email.startswith("default"):
        return "Not Found"
    if email.startswith("defeault"):
        return "Not Found"
    return email if re.match(r"[^@]+@[^@]+\.[a-zA-Z]{2,}", email) else "Not Found"

#===============================================================================================================================>
    #Format message for including/excluding name
def message_content(add_name,recipient_name,msg_content,sender,sender_div):
    if add_name == 'on':
        message = f"Hello {recipient_name}!, {msg_content}\n\n{sender}\n{sender_div}"
    else:
        message = f"Hello, {msg_content}\n\n{sender}\n{sender_div}"
    return message

#===============================================================================================================================>
    #Create status data for message logs status
def get_status_data(recipient_name,recipient_contact,message):
    status_data = f"{recipient_name}:{recipient_contact}:{message}"
    return status_data

#===============================================================================================================================>
    #Display HR data to directory
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
        return (url,payload,headers)

#===============================================================================================================================>
    #Upload file and search in hr data
def convert_file_to_inputs(file):
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
    
    if file:
        for line in file.stream.read().decode("utf-8").splitlines():
            account_number = line[:10].strip()
            account_name = line[10:50].strip().lower()
            raw_names.append(account_name)
            name_search = account_name.replace(" ", "").replace(",", "").replace(".", "")

            if account_number == "9999999999":
                break
            data_list.append(account_number)
            name_list.append(name_search)

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            query = f"SELECT first_name, last_name, middle_name, email, mobile_no, account_number FROM {DB_TABLE}"
            cursor.execute(query)
            raw_data = cursor.fetchall()
            
            matched_names = set()

            for row in raw_data:
                db_fn = row["first_name"] if row["first_name"] else ""
                db_mn = row["middle_name"] if row["middle_name"] else ""
                db_ln = row["last_name"] if row["last_name"] else ""

                format_name = f"{db_ln}{db_fn}"
                db_format_name = format_name.replace(" ", "").replace(",", "").replace(".", "").lower()
                
                for file_name in name_list:
                    if db_format_name in file_name or file_name in db_format_name:
                        matched_names.add(file_name)

                        first_name = row["first_name"] if row["first_name"] else ""
                        middle_name = row["middle_name"] if row["middle_name"] else ""
                        last_name = row["last_name"] if row["last_name"] else ""
                        fullname = f"{last_name}, {first_name} {middle_name}".strip()
                        
                        
                        print("Match found:")
                        print("Account Number:", row["account_number"])
                        print("Full Name:", fullname)
                        print("First Name:", first_name)
                        print("Mobile:", format_mobile_number(row["mobile_no"]))
                        print("Email:", format_email(row["email"]))
                        print("-\n\n")
                        
            for i, name in enumerate(name_list):
                if name not in matched_names:
                    print(f"Not found: {raw_names[i].upper()}")  # Print original format

    finally:
        connection.close()