#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.message_temp import Msg_templates
from extensions import db
from flask import request, flash
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_msg_temp():
    msg_temp_name = request.form.get('msg_temp_name')
    if msg_temp_name:
        existing_msg_temp = Msg_templates.query.filter_by(msg_temp_name=msg_temp_name).first()
        if existing_msg_temp:
            flash('Template already exists', 'error')
            return None 
    msg_temp_description = request.form.get('msg_temp_description')
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_msg_temp = Msg_templates(
        msg_temp_name=msg_temp_name,
        msg_temp_description=msg_temp_description,
        created_by=created_by,
        created_on=created_on
    )
    try:
        db.session.add(new_msg_temp)
        db.session.commit()
        return new_msg_temp 
    except Exception as e:
        db.session.rollback()
        return None 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>   
def edit_msg_temp(msg_temp_id):
    msg_temp = Msg_templates.get_by_id(msg_temp_id)
    
    msg_temp_name = request.form.get('msg_temp_name')
    if msg_temp_name:
        existing_msg_temp = Msg_templates.query.filter_by(msg_temp_name=msg_temp_name).first()
        if existing_msg_temp and existing_msg_temp.msg_temp_id != msg_temp_id:
            flash('msg_temp already exists', 'error')
            return None 
        msg_temp.msg_temp_name = msg_temp_name

    msg_temp.msg_temp_description = request.form.get('msg_temp_description', msg_temp.msg_temp_description)
    msg_temp.updated_by = current_user.full_name
    msg_temp.updated_on = get_manila_time()
    
    try:
        msg_temp.save()
        return msg_temp 
    except Exception as e:
        db.session.rollback()
        return None

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>
def delete_msg_temp(msg_temp_id):
    msg_temp = Msg_templates.get_by_id(msg_temp_id)
    if not msg_temp:
        return False 
    try:
        db.session.delete(msg_temp)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

#===============================================================================================================================>