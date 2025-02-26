from datetime import datetime
import pytz
import pymysql
import random
from flask import g
from models.hrpears_credentials import Hrpears

def get_manila_time():
    manila_tz = pytz.timezone('Asia/Manila')
    utc_time = datetime.now(pytz.utc)
    manila_time = utc_time.astimezone(manila_tz)
    return manila_time.strftime('%a, %b-%d-%Y ; %I:%M%p').lower()

def to_block_text(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    blocky = ["🅰", "🅱", "🅲", "🅳", "🅴", "🅵", "🅶", "🅷", "🅸", "🅹", "🅺", "🅻", "🅼", "🅽", "🅾", "🅿", "🆀", "🆁", "🆂", "🆃", "🆄", "🆅", "🆆", "🆇", "🆈", "🆉"]

    return ''.join(blocky[normal.index(char)] if char in normal else char for char in text.upper())

def generate_tracker(sender_div, msg_type):
    random_number = random.randint(1, 9999)
    tracking_number = f"{sender_div}-{msg_type}:{random_number}"
    return tracking_number


def get_table_data():
    
    hris_id = g.sys_settings.hris_api_id if g.sys_settings and g.sys_settings.hris_api_id else 1
    hris_data = Hrpears.get_by_id(hris_id)
    
    DB_HOST = hris_data.hrpears_host
    DB_USER = hris_data.hrpears_user
    DB_PASSWORD = hris_data.hrpears_password
    DB_NAME = hris_data.hrpears_dbname
    DB_TABLE = hris_data.hrpears_table

    # Connect to the database
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Query to fetch required data
            query = f"SELECT first_name, last_name, middle_name, email, mobile_no FROM {DB_TABLE}"
            cursor.execute(query)
            data = cursor.fetchall()
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
    return data    