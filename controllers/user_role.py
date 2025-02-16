from models.user_role import Roles
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

def add_role():
    role_name = request.form.get('role_name')
    role_description = request.form.get('role_description')
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_roles = Roles(
        role_name=role_name,
        role_description=role_description,
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_roles)
    db.session.commit()

    flash("Role added successfully", "success")
    return new_roles 
    
def edit_role(role_id):
    role = Roles.get_by_id(role_id)
    
    role_name = request.form.get('role_name',role.role_name)
    role_description = request.form.get('role_description',role.role_description)
    updated_by = current_user.full_name
    updated_on = get_manila_time()
   
    role.role_name = role_name
    role.role_description = role_description
    role.updated_by = updated_by
    role.updated_on = updated_on
    
    try:
        role.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_role(role_id):
    role = Roles.get_by_id(role_id)
    try:
        db.session.delete(role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
