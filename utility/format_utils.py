#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
import re
from flask import g
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
    #Format amount with separator comma every thousand'
def format_amount(amount):
    try:
        return f"{float(amount):,.2f}"  
    except ValueError:
        return "Invalid amount"
#===============================================================================================================================>
