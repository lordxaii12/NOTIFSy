#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from datetime import datetime
import pytz
from flask import g
from config import Config
from cryptography.fernet import Fernet
from models.hrpears_credentials import Hrpears
import pymysql
from extensions import db, cache
from msg_utils import format_email, format_mobile_number
#===============================================================================================================================>
    #Get datetime in manila based timezone
def get_manila_time():
    manila_tz = pytz.timezone('Asia/Manila')
    utc_time = datetime.now(pytz.utc)
    manila_time = utc_time.astimezone(manila_tz)
    return manila_time.strftime('%a, %b-%d-%Y ; %I:%M%p').lower()
#===============================================================================================================================>
    #Convert "text" to "🆃🅴🆇🆃"
def to_block_text(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    blocky = ["🅰", "🅱", "🅲", "🅳", "🅴", "🅵", "🅶", "🅷", "🅸", "🅹", "🅺", "🅻", "🅼", "🅽", "🅾", "🅿", "🆀", "🆁", "🆂", "🆃", "🆄", "🆅", "🆆", "🆇", "🆈", "🆉"]

    return ''.join(blocky[normal.index(char)] if char in normal else char for char in text.upper())
#===============================================================================================================================>
    #Encrypt data
def encrypt_content(content):
     encrypted_text = Config.cipher.encrypt(content.encode()).decode()
     return encrypted_text
#===============================================================================================================================>
    #Decrypt data
def decrypt_content(content):
     decrypted_text = Config.cipher.decrypt(content.encode()).decode()
     return decrypted_text
#===============================================================================================================================>
#===============================================================================================================================>
    #Display HR data to registration directory
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