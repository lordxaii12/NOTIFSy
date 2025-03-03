#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.user import User_v1
from extensions import db
from flask import request,flash
from flask_login import current_user
from utility.sys_utils import get_manila_time

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
    division = request.form.get('division')
    role_id = request.form.get('role_id')
    
    theme_id = 1
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_user = User_v1(
        username=username,
        full_name=full_name,
        division=division,
        role_id=role_id,
        theme_id=theme_id,
        
        created_by=created_by,
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
    username = request.form.get('username')
    if username:
        existing_user = User_v1.query.filter_by(username=username).first()
        if existing_user and existing_user.user_id != user_id:
            flash('Username already exists', 'error')
            return None 
        user.username = username
    full_name = request.form.get('full_name')
    if full_name:
        existing_full_name = User_v1.query.filter_by(full_name=full_name).first()
        if existing_full_name and existing_full_name.user_id != user_id:
            flash('Full Name already exists', 'error')
            return None 
        user.full_name = full_name
    user.division = request.form.get('division', user.division)
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