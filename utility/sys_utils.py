#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from datetime import datetime
import pytz
from flask import g
from config import Config

from cryptography.fernet import Fernet
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
