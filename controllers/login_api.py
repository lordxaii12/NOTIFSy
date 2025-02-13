from models.login_api import LogApi
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

def add_login_api():
    login_api_url = request.form.get('login_api_url')
    login_api_token = request.form.get('login_api_token')
    login_api_content_type = request.form.get('login_api_content_type')
       
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_login_api = LogApi(
        login_api_url=login_api_url,
        login_api_token=login_api_token,
        login_api_content_type=login_api_content_type,
        
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_login_api)
    db.session.commit()

    flash("API added successfully", "success")
    return new_login_api 
    
def edit_login_api(login_api_id):
    log_api = LogApi.get_by_id(login_api_id)
    
    login_api_url = request.form.get('login_api_url',log_api.login_api_url)
    login_api_token = request.form.get('login_api_token',log_api.login_api_token)
    login_api_content_type = request.form.get('login_api_content_type',log_api.login_api_content_type)
    
    updated_by = current_user.full_name
    updated_on = get_manila_time()
   
    log_api.login_api_url = login_api_url
    log_api.login_api_token = login_api_token
    log_api.login_api_content_type = login_api_content_type
    
    log_api.updated_by = updated_by
    log_api.updated_on = updated_on
    
    try:
        log_api.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_login_api(role_id):
    log_api = LogApi.get_by_id(role_id)
    try:
        db.session.delete(log_api)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
