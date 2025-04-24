#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.user_division import Divisions
from extensions import db
from flask import request, flash
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_division():
    division_name = request.form.get('division_name')
    if division_name:
        existing_division = Divisions.query.filter_by(division_name=division_name).first()
        if existing_division:
            flash('Division already exists', 'error')
            return None 
    division_description = request.form.get('division_description')
    created_by = current_user.full_name
    created_on = get_manila_time()
    division_credits = 0

    new_division = Divisions(
        division_name=division_name,
        division_description=division_description,
        division_credits=division_credits,
        created_by=created_by,
        created_on=created_on
    )
    try:
        db.session.add(new_division)
        db.session.commit()
        return new_division 
    except Exception as e:
        db.session.rollback()
        return None 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>   
def edit_division(division_id):
    division = Divisions.get_by_id(division_id)
    
    division_name = request.form.get('division_name')
    if division_name:
        existing_division = Divisions.query.filter_by(division_name=division_name).first()
        if existing_division and existing_division.division_id != division_id:
            flash('Division already exists', 'error')
            return None 
        division.division_name = division_name

    division.division_description = request.form.get('division_description', division.division_description)
    division.updated_by = current_user.full_name
    division.updated_on = get_manila_time()
    
    try:
        division.save()
        return division 
    except Exception as e:
        db.session.rollback()
        return None

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>
def delete_division(division_id):
    division = Divisions.get_by_id(division_id)
    if not division:
        return False 
    try:
        db.session.delete(division)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

#===============================================================================================================================>