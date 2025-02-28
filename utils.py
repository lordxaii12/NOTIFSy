#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from datetime import datetime
import pytz
import random
from flask import g
import re

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
        
    if mobile_no.startswith("09000"): 
        return "Not Found"
    
    if not mobile_no.startswith("0"):
        mobile_no = "0" + mobile_no
    if mobile_no == "0" * 11:
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





