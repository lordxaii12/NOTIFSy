#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.itexmo_credentials import Itexmo
from extensions import db
from flask import request
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_itexmo():
    itexmo_name = request.form.get('itexmo_name')
    itexmo_url = request.form.get('itexmo_url')
    itexmo_email = request.form.get('itexmo_email')
    itexmo_password = request.form.get('itexmo_password')
    itexmo_apicode = request.form.get('itexmo_apicode')
    itexmo_contenttype = request.form.get('itexmo_contenttype')

    created_by = current_user.full_name
    created_on = get_manila_time()

    new_itexmo = Itexmo(
        itexmo_name=itexmo_name,
        itexmo_url=itexmo_url,
        itexmo_email=itexmo_email,
        itexmo_password=itexmo_password,
        itexmo_apicode=itexmo_apicode,
        itexmo_contenttype=itexmo_contenttype,
        
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_itexmo)
    db.session.commit()

    return new_itexmo 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>   
def edit_itexmo(itexmo_id):
    itexmo = Itexmo.get_by_id(itexmo_id)
    itexmo.itexmo_name = request.form.get('itexmo_name', itexmo.itexmo_name)
    itexmo.itexmo_url = request.form.get('itexmo_url', itexmo.itexmo_url)
    itexmo.itexmo_email = request.form.get('itexmo_email', itexmo.itexmo_email)
    itexmo.itexmo_password = request.form.get('itexmo_password', itexmo.itexmo_password)
    itexmo.itexmo_apicode = request.form.get('itexmo_apicode', itexmo.itexmo_apicode)
    itexmo.itexmo_contenttype = request.form.get('itexmo_contenttype', itexmo.itexmo_contenttype)
    
    itexmo.updated_by = current_user.full_name
    itexmo.updated_on = get_manila_time()

    try:
        itexmo.save()
        return itexmo  
    except Exception as e:
        db.session.rollback()
        return None  

#===============================================================================================================================>
#
#================ CREDITS CHECKER ==============================================================================================>
def credits_check (itexmo_id, credits_remaining, credits_consumed):
    itexmo = Itexmo.get_by_id(itexmo_id)
    itexmo.credits_remaining = credits_remaining
    itexmo.credits_consumed = credits_consumed
    try:
        itexmo.save()
        return itexmo  
    except Exception as e:
        db.session.rollback()
        return None

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>    
def delete_itexmo(itexmo_id):
    itexmo = Itexmo.get_by_id(itexmo_id)
    try:
        db.session.delete(itexmo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

#===============================================================================================================================>