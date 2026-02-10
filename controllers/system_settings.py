#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.system_settings import SysSettings
from extensions import db
from flask import request,flash
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_sys_setting():
    sys_name = request.form.get('sys_name')
    if sys_name:
        existing_sys_name = SysSettings.query.filter_by(sys_name=sys_name).first()
        if existing_sys_name:
            flash('Settings name already exists', 'error')
            return None
    sys_app_name = request.form.get('sys_app_name')
    sys_app_user = request.form.get('sys_app_user')
    sys_app_email = request.form.get('sys_app_email')
    sys_app_phone = request.form.get('sys_app_phone')
    
    sys_app_user_text = request.form.get('sys_app_user_text')
    sys_app_role_text = request.form.get('sys_app_role_text')
    sys_app_division_text = request.form.get('sys_app_division_text')
    sys_app_logs_text = request.form.get('sys_app_logs_text')
    
    sys_app_itexmo_credits_url = request.form.get('sys_app_itexmo_credits_url')
    sys_app_eprocsys_supplier_url = request.form.get('sys_app_eprocsys_supplier_url')
    
    sys_app_aics_supplier_url = request.form.get('sys_app_aics_supplier_url')
    sys_app_aics_supplier_token = request.form.get('sys_app_aics_supplier_token')
    
    msg_api_id = request.form.get('msg_api_id')
    email_api_id = request.form.get('email_api_id')
    hris_api_id = request.form.get('hris_api_id')
    login_api_id = request.form.get('login_api_id')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_sys_setting = SysSettings(
        sys_name=sys_name,
        sys_app_name=sys_app_name,
        sys_app_user=sys_app_user,
        sys_app_email=sys_app_email,
        sys_app_phone=sys_app_phone,
        
        sys_app_user_text=sys_app_user_text,
        sys_app_role_text=sys_app_role_text,
        sys_app_division_text=sys_app_division_text,
        sys_app_logs_text=sys_app_logs_text,
        
        sys_app_itexmo_credits_url=sys_app_itexmo_credits_url,
        sys_app_eprocsys_supplier_url=sys_app_eprocsys_supplier_url,
        sys_app_aics_supplier_url=sys_app_aics_supplier_url,
        sys_app_aics_supplier_token=sys_app_aics_supplier_token,
        
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

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>     
def edit_sys_setting(sys_setting_id):
    sys_setting = SysSettings.get_by_id(sys_setting_id)
    sys_name = request.form.get('sys_name')
    if sys_name:
        existing_sys_name = SysSettings.query.filter_by(sys_name=sys_name).first()
        if existing_sys_name and existing_sys_name.sys_setting_id != sys_setting_id:
            flash('Username already exists', 'error')
            return None 
        sys_setting.sys_name = sys_name
        
    sys_setting.sys_app_name = request.form.get('sys_app_name', sys_setting.sys_app_name)
    sys_setting.sys_app_user = request.form.get('sys_app_user', sys_setting.sys_app_user)
    sys_setting.sys_app_email = request.form.get('sys_app_email', sys_setting.sys_app_email)
    sys_setting.sys_app_phone = request.form.get('sys_app_phone', sys_setting.sys_app_phone)
    
    sys_setting.sys_app_user_text = request.form.get('sys_app_user_text', sys_setting.sys_app_user_text)
    sys_setting.sys_app_role_text = request.form.get('sys_app_role_text', sys_setting.sys_app_role_text)
    sys_setting.sys_app_division_text = request.form.get('sys_app_division_text', sys_setting.sys_app_division_text)
    sys_setting.sys_app_logs_text = request.form.get('sys_app_logs_text', sys_setting.sys_app_logs_text)
    
    sys_setting.sys_app_itexmo_credits_url = request.form.get('sys_app_itexmo_credits_url', sys_setting.sys_app_itexmo_credits_url)
    sys_setting.sys_app_eprocsys_supplier_url = request.form.get('sys_app_eprocsys_supplier_url', sys_setting.sys_app_eprocsys_supplier_url)
    
    sys_setting.sys_app_aics_supplier_url = request.form.get('sys_app_aics_supplier_url', sys_setting.sys_app_aics_supplier_url)
    sys_setting.sys_app_aics_supplier_token = request.form.get('sys_app_aics_supplier_token', sys_setting.sys_app_aics_supplier_token)
    
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

#===============================================================================================================================>
#
#================ EDIT SYSTEM NOTICE ===========================================================================================> 
def edit_system_notice(sys_setting_id):
    sys_setting = SysSettings.get_by_id(sys_setting_id)
    sys_setting.system_notice =  request.form.get('notice', sys_setting.system_notice)
    try:
        sys_setting.save()
        return sys_setting
    except Exception as e:
        db.session.rollback()
        return None

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================> 
def delete_sys_setting(sys_setting_id):
    sys_setting = SysSettings.get_by_id(sys_setting_id)
    try:
        db.session.delete(sys_setting)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

#===============================================================================================================================>