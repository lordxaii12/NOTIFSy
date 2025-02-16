from models.user_themes import Theme
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

def add_theme():
    theme_name = request.form.get('theme_name')
    theme_description = request.form.get('theme_description')
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_themes = Theme(
        theme_name=theme_name,
        theme_description=theme_description,
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_themes)
    db.session.commit()

    flash("Theme added successfully", "success")
    return new_themes 
    
def edit_theme(theme_id):
    theme = Theme.get_by_id(theme_id)
    
    theme_name = request.form.get('theme_name',theme.theme_name)
    theme_description = request.form.get('theme_description',theme.theme_description)
    updated_by = current_user.full_name
    updated_on = get_manila_time()
   
    theme.theme_name = theme_name
    theme.theme_description = theme_description
    theme.updated_by = updated_by
    theme.updated_on = updated_on
    
    try:
        theme.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_theme(theme_id):
    theme = Theme.get_by_id(theme_id)
    try:
        db.session.delete(theme)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
