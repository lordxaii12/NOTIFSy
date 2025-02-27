#--CODE BY: RYRUBIO--#
#===============================================================================================================================>
from datetime import datetime
import pytz
import random
from flask import g

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