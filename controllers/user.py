#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.user import User_v1
from extensions import db
from flask import request,flash
from flask_login import current_user
from utility.sys_utils import get_manila_time, encrypt_content

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_user():
    username = request.form.get('username')
    if username:
        existing_user = User_v1.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return None 
    full_name = request.form.get('full_name')
    if full_name:
        existing_fullname = User_v1.query.filter_by(full_name=full_name).first()
        if existing_fullname:
            flash('Full Name already exists', 'error')
            return None
    role_id = request.form.get('role_id')
    
    theme_id = 1
    credit_used = 0
    login_status = 0
    login_error_counter = 0
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_user = User_v1(
        username=encrypt_content(username),
        full_name=encrypt_content(full_name),
        role_id=role_id,
        theme_id=theme_id,
        credit_used=credit_used,
        login_status=login_status,
        login_error_counter=login_error_counter,
        
        created_by=encrypt_content(created_by),
        created_on=created_on
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user 
    except Exception as e:
        db.session.rollback()
        return None 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>   
def edit_user(user_id):
    user = User_v1.get_by_id(user_id)
    user.role_id = request.form.get('role_id', user.role_id)
    
    user.updated_by = current_user.full_name
    user.updated_on = get_manila_time()
    try:
        user.save()
        return user 
    except Exception as e:
        db.session.rollback()
        return None 
#===============================================================================================================================>
#
#================ EDIT CREDITUSED ==============================================================================================>
def edit_credit_used(user_id, credit_used):
    user = User_v1.get_by_id(user_id)
    user.credit_used = credit_used
    try:
        user.save()
        return user
    except Exception as e:
        db.session.rollback()
        return None

#===============================================================================================================================>
#
#================ EDIT USER NOTES ==============================================================================================>
def edit_user_notes(user_id):
    user = User_v1.get_by_id(user_id)
    user.user_notes = request.form.get('notes', user.user_notes)
    try:
        user.save()
        return user
    except Exception as e:
        db.session.rollback()
        return None


#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>
def delete_user(user_id):
    user = User_v1.get_by_id(user_id)
    if not user:
        return False 
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

#===============================================================================================================================>