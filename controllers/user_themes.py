#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.user_themes import Theme
from extensions import db
from flask import request
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_theme():
    theme_name = request.form.get('theme_name')
    theme_description = request.form.get('theme_description')
    
    theme_bg = request.form.get('theme_bg')
    theme_font = request.form.get('theme_font')
    theme_icon = request.form.get('theme_icon')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_themes = Theme(
        theme_name=theme_name,
        theme_description=theme_description,

        theme_bg=theme_bg,
        theme_font=theme_font,
        theme_icon=theme_icon,
        
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_themes)
    db.session.commit()
    return new_themes 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>   
def edit_theme(theme_id):
    theme = Theme.get_by_id(theme_id)
    
    theme.theme_name = request.form.get('theme_name',theme.theme_name)
    theme.theme_description = request.form.get('theme_description',theme.theme_description)
    
    theme.theme_bg = request.form.get('theme_bg',theme.theme_bg)
    theme.theme_font = request.form.get('theme_font',theme.theme_font)
    theme.theme_icon = request.form.get('theme_icon',theme.theme_icon)
    
    theme.updated_by = current_user.full_name
    theme.updated_on = get_manila_time()
   
    try:
        theme.save()
        return theme
    except Exception as e:
        db.session.rollback()
        return None

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>
def delete_theme(theme_id):
    theme = Theme.get_by_id(theme_id)
    try:
        db.session.delete(theme)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

#===============================================================================================================================>