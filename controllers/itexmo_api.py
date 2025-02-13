from models.itexmo_api import Itexmo
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

def add_itexmo():
    itexmo_url = request.form.get('itexmo_url')
    itexmo_email = request.form.get('itexmo_email')
    itexmo_password = request.form.get('itexmo_password')
    itexmo_apicode = request.form.get('itexmo_apicode')
    itexmo_contenttype = request.form.get('itexmo_contenttype')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_itexmo = Itexmo(
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

    flash("itexmo added successfully", "success")
    return new_itexmo 
    
def edit_itexmo(itexmo_id):
    itexmo = Itexmo.get_by_id(itexmo_id)
    if not itexmo:
        return None
    itexmo.itexmo_url = request.form.get('itexmo_url',itexmo.itexmo_url)
    itexmo.itexmo_email = request.form.get('itexmo_email',itexmo.itexmo_email)
    itexmo.itexmo_password = request.form.get('itexmo_password',itexmo.itexmo_password)
    itexmo.itexmo_apicode = request.form.get('itexmo_apicode',itexmo.itexmo_apicode)
    itexmo.itexmo_contenttype = request.form.get('itexmo_contenttype',itexmo.itexmo_contenttype)
    
    itexmo.updated_by = current_user.full_name
    itexmo.updated_on = get_manila_time()
   
   
    try:
        itexmo.save()
    except Exception as e:
        db.session.rollback()
        flash('iTexMo record not found or update failed', 'error')

def delete_itexmo(itexmo_id):
    itexmo = Itexmo.get_by_id(itexmo_id)
    try:
        db.session.delete(itexmo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
