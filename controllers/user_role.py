#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.user_role import Roles
from extensions import db
from flask import request, flash
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_role():
    role_name = request.form.get('role_name')
    if role_name:
        existing_role = Roles.query.filter_by(role_name=role_name).first()
        if existing_role:
            flash('User Type already exists', 'error')
            return None 
    role_description = request.form.get('role_description')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_roles = Roles(
        role_name=role_name,
        role_description=role_description,
        created_by=created_by,
        created_on=created_on
    )

    try:
        db.session.add(new_roles)
        db.session.commit()
        return new_roles 
    except Exception as e:
        db.session.rollback()
        return None 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>    
def edit_role(role_id):
    role = Roles.get_by_id(role_id)
    
    role_name = request.form.get('role_name')
    
    if role_name:
        existing_role = Roles.query.filter_by(role_name=role_name).first()
        if existing_role and existing_role.role_id != role_id:
            flash('User type already exists', 'error')
            return None 
        role.role_name = role_name
    
    role.role_description = request.form.get('role_description',role.role_description)
    role.updated_by = current_user.full_name
    role.updated_on = get_manila_time()
   
    try:
        role.save()
        return role 
    except Exception as e:
        db.session.rollback()
        return None 

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>
def delete_role(role_id):
    role = Roles.get_by_id(role_id)
    if not role:
        return False 
    try:
        db.session.delete(role)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

#===============================================================================================================================>