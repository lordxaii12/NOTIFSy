from models.user_division import Divisions
from extensions import db
from flask import request, jsonify
from flask_login import current_user
from utils import get_manila_time

def add_division():
    division_name = request.form.get('division_name')
    division_description = request.form.get('division_description')
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_divisions = Divisions(
        division_name=division_name,
        division_description=division_description,
        created_by=created_by,
        created_on=created_on
    )
    try:
        new_divisions.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
def edit_division(division_id):
    division = Divisions.get_by_id(division_id)
    
    division_name = request.form.get('division_name',division.division_name)
    division_description = request.form.get('division_description',division.division_description)
    updated_by = current_user.full_name
    updated_on = get_manila_time()
   
    division.division_name = division_name
    division.division_description = division_description
    division.updated_by = updated_by
    division.updated_on = updated_on
    
    try:
        division.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_division(division_id):
    division = Divisions.get_by_id(division_id)
    try:
        db.session.delete(division)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
