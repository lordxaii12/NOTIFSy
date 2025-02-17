from models.system_settings import SysSettings
from extensions import db
from flask import request
from flask_login import current_user
from utils import get_manila_time

def add_sys_setting():
    sys_app_name = request.form.get('sys_app_name')
    sys_app_user = request.form.get('sys_app_user')
    sys_app_email = request.form.get('sys_app_email')
    sys_app_phone = request.form.get('sys_app_phone')
    
    msg_api_id = request.form.get('msg_api_id')
    email_api_id = request.form.get('email_api_id')
    hris_api_id = request.form.get('hris_api_id')
    login_api_id = request.form.get('login_api_id')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_sys_setting = SysSettings(
        
        sys_app_name=sys_app_name,
        sys_app_user=sys_app_user,
        sys_app_email=sys_app_email,
        sys_app_phone=sys_app_phone,
        
        msg_api_id=msg_api_id,
        email_api_id=email_api_id,
        hris_api_id=hris_api_id,
        login_api_id=login_api_id,
        
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_sys_setting)
    db.session.commit()

    return new_sys_setting 
    
def edit_sys_setting(sys_setting_id):
    sys_setting = SysSettings.get_by_id(sys_setting_id)
    sys_setting.sys_app_name = request.form.get('sys_app_name', sys_setting.sys_app_name)
    sys_setting.sys_app_user = request.form.get('sys_app_user', sys_setting.sys_app_user)
    sys_setting.sys_app_email = request.form.get('sys_app_email', sys_setting.sys_app_email)
    sys_setting.sys_app_phone = request.form.get('sys_app_phone', sys_setting.sys_app_phone)
    
    sys_setting.msg_api_id = request.form.get('msg_api_id', sys_setting.msg_api_id)
    sys_setting.email_api_id = request.form.get('email_api_id', sys_setting.email_api_id)
    sys_setting.hris_api_id = request.form.get('hris_api_id', sys_setting.hris_api_id)
    sys_setting.login_api_id = request.form.get('login_api_id', sys_setting.login_api_id)
    
    sys_setting.updated_by = current_user.full_name
    sys_setting.updated_on = get_manila_time()

    try:
        sys_setting.save()
        return sys_setting  
    except Exception as e:
        db.session.rollback()
        return None  
    
def delete_sys_setting(sys_setting_id):
    sys_setting = SysSettings.get_by_id(sys_setting_id)
    try:
        db.session.delete(sys_setting)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
