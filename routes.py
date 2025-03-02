#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify
from flask_login import login_required, logout_user
from flask_migrate import Migrate
from config import Config
from flask_login import login_user, current_user
from utils import get_manila_time, message_content, generate_tracker, extract_first_name, format_mobile_number, format_email, get_status_data
import requests
from extensions import db, limiter
import json
#===============================================================================================================================>
#Models
from models.user import User_v1
from models.user_role import Roles
from models.user_logs import User_logs
from models.user_division import Divisions
from models.external_contacts import External
from models.login_credentials import LogApi
from models.user_themes import Theme
from models.itexmo_credentials import Itexmo
from models.email_credentials import Ecredss
from models.hrpears_credentials import Hrpears
from models.system_settings import SysSettings
from models.msg_log import Msg_log
#===============================================================================================================================>
#Controllers
from controllers.user_role import add_role, edit_role, delete_role
from controllers.user import add_user, edit_user, delete_user
from controllers.user_logs import add_user_logs, delete_user_logs
from controllers.user_division import add_division, edit_division, delete_division
from controllers.external_contacts import add_external, edit_external, delete_external
from controllers.login_credentials import add_login_api, edit_login_api, delete_login_api
from controllers.user_themes import add_theme, edit_theme, delete_theme
from controllers.itexmo_credentials import add_itexmo, edit_itexmo, delete_itexmo
from controllers.email_credentials import add_ecreds, delete_ecreds, edit_ecreds
from controllers.hrpears_credentials import add_hrpears, edit_hrpears, delete_hrpears
from controllers.system_settings import edit_sys_setting
from controllers.msg_log import add_msg_log, delete_msg_log, send_msg, get_table_data
#===============================================================================================================================>
notifs = Blueprint('notifs', __name__, template_folder='templates')
#===============================================================================================================================>
#
#
#
#================ Admin ========================================================================================================>
@notifs.route('/admin', methods=['GET', 'POST'])#admin page
@login_required
def admin():
    itexmo_data = Itexmo.get_all()
    total_itexmo_data = len(itexmo_data)
    
    email_data = Ecredss.get_all()
    total_email_data = len(email_data)
    
    hrpears_data = Hrpears.get_all()
    total_hrpears_data = len(hrpears_data)
    
    login_data = LogApi.get_all()
    total_login_data = len(login_data)
    
    user_data = User_v1.get_all()
    total_user = len(user_data)
    
    role_data = Roles.get_all()
    total_role = len(role_data)
    
    division_data = Divisions.get_all()
    total_division = len(division_data)
    
    log_data = User_logs.get_all()
    total_log = len(log_data)
    
    sys_settings_data = SysSettings.get_by_id(1)
    
    return render_template('admin.html',
                           role_data=role_data,
                           total_role=total_role,
                           user_data=user_data,
                           total_user=total_user,
                           itexmo_data=itexmo_data,
                           total_itexmo_data=total_itexmo_data,
                           email_data=email_data,
                           total_email_data=total_email_data,
                           hrpears_data=hrpears_data,
                           total_hrpears_data=total_hrpears_data,
                           login_data=login_data,
                           total_login_data=total_login_data,
                           division_data=division_data,
                           total_division=total_division,
                           log_data=log_data,
                           total_log=total_log,
                           sys_settings_data=sys_settings_data)

@notifs.route('/edit_system_settings_route/<int:sys_setting_id>', methods=['POST'])#edit system settings
@login_required
def edit_system_settings_route(sys_setting_id):
    try:
        if edit_sys_setting(sys_setting_id):
            flash('System settings updated successfully,  LOGOUT TO APPLY CHANGES.', 'success')
        else:
            flash('System settings not found or update failed', 'error')
            return redirect(url_for('notifs.admin'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
    return redirect(url_for('notifs.admin'))

@notifs.route('/login', methods=['GET', 'POST'])#Login
# @limiter.limit("5 per minute")
def login():
    log_inCreds = LogApi.get_by_id(1)
    url = log_inCreds.login_api_url.strip()
    token = log_inCreds.login_api_token.strip()
    content_type = log_inCreds.login_api_content_type.strip()
    
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User_v1.query.filter_by(username=username).first()
            
            if user:
                headers = {
                    "X-Token": token,
                    "Content-Type": content_type
                }
                data = {
                    "username": username,
                    "password": password
                }
                response = requests.post(url, data=data, headers=headers)
                
                if response.status_code == 200:
                    login_user(user)
                    user.cur_login = get_manila_time()
                    db.session.commit()
                    flash('Login successful!', 'success')
                    return redirect(url_for('notifs.home'))
                else:
                    flash('Invalid username or password', 'error')
            else:
                flash('Invalid username or password', 'error')
        return render_template('login.html')

    except requests.exceptions.RequestException:
        flash('There was an issue with the login request.', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    return render_template('login.html')

@notifs.route('/logout')#Logout
@login_required
def logout():
    current_user.last_logout = get_manila_time()
    login_session = current_user.cur_login
    if login_session:
        current_user.last_login = current_user.cur_login
        db.session.commit()
    else:
        current_user.last_login = get_manila_time()
        db.session.commit()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('notifs.login'))

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_itexmo', methods=['POST'])#add itexmo credentials
@login_required
def register_itexmo():
    try:
        new_itexmo = add_itexmo()  
        if new_itexmo:
            activity = f"ADDED {new_itexmo.itexmo_name} to Itexmo Credentials."
            flash('iTexMo credentials added successfully!', 'success')
        else:
            activity = f"FAILED TO ADD iTexMo Credentials. Missing or invalid data."
            flash('Failed to add iTexMo credentials.', 'error')
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()

    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD iTexMo Credentials due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))

@notifs.route('/edit_itexmo_route/<int:itexmo_id>', methods=['POST'])#edit itexmo credentials
@login_required
def edit_itexmo_route(itexmo_id):
    creds_data = Itexmo.get_by_id(itexmo_id)
    cur_name = creds_data.itexmo_name
    cur_url = creds_data.itexmo_url
    cur_email = creds_data.itexmo_email
    cur_pass = creds_data.itexmo_password
    cur_apicode = creds_data.itexmo_apicode
    cur_contenttype = creds_data.itexmo_contenttype
    
    new_name = request.form.get('itexmo_name')
    new_url = request.form.get('itexmo_url')
    new_email = request.form.get('itexmo_email')
    new_pass = request.form.get('itexmo_password')
    new_apicode = request.form.get('itexmo_apicode')
    new_contenttype = request.form.get('itexmo_contenttype')
    try:
        if edit_itexmo(itexmo_id):
            activity = f"EDIT Itexmo Credentials from: [{cur_name},{cur_url},{cur_email},{cur_pass},{cur_apicode},{cur_contenttype}]to [{new_name},{new_url},{new_email},{new_pass},{new_apicode},{new_contenttype}]."
            flash('iTexMo Credential updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT iTexMo Credentials. Missing or invalid data."
            flash('iTexMo record not found or update failed', 'error')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EIDT iTexMo Credentials due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_itexmo/<int:itexmo_id>', methods=['POST'])#delete itexmo credentials
@login_required
def delete_itexmo_route(itexmo_id):
    creds_data = Itexmo.get_by_id(itexmo_id)
    try:
        delete_itexmo(itexmo_id)
        activity = f"DELETE {creds_data.itexmo_name} from Itexmo Credentials."
        flash('iTexMo record deleted successfully', 'success')
    except Exception as e:
        activity = f"FAILED TO DELETE iTexMo Credentials due to error: {str(e)}."
        flash('An error occurred while deleting the record.', 'error')
    add_user_logs(activity)
    db.session.commit()
    return redirect(request.referrer)

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_login_api', methods=['POST'])#add login API credentials
@login_required
def register_login_api():
    try:
        new_login_api = add_login_api()  
        if new_login_api:
            activity = f"ADDED {new_login_api.login_api_name} to Login API Credentials."
            flash('Login API credentials added successfully!', 'success')
        else:
            activity = f"FAILED TO ADD Login API Credentials. Missing or invalid data."
            flash('Failed to add Login API credentials.', 'error')
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD Login API Credentials due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))

@notifs.route('/edit_loginapi_route/<int:login_api_id>', methods=['POST'])#edit login API credentials
@login_required
def edit_loginapi_route(login_api_id):
    loginapi_data = LogApi.get_by_id(login_api_id)
    cur_name = loginapi_data.login_api_name
    cur_url = loginapi_data.login_api_url
    cur_token = loginapi_data.login_api_token
    cur_contenttype = loginapi_data.login_api_content_type
    
    new_name = request.form.get('login_api_name')
    new_url = request.form.get('login_api_url')
    new_token = request.form.get('login_api_token')
    new_contenttype = request.form.get('login_api_content_type')
    try:
        if edit_login_api(login_api_id):
            activity = f"EDIT Login API Credentials from: [{cur_name},{cur_url},{cur_token},{cur_contenttype}]to [{new_name},{new_url},{new_token},{new_contenttype}]."
            flash('Login API Credential updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT Login API Credentials. Missing or invalid data."
            flash('Login API record not found or update failed', 'error')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EDIT Login API Credentials due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_loginapi_route/<int:login_api_id>', methods=['POST'])#delete login API credentials
@login_required
def delete_loginapi_route(login_api_id):
    loginapi_data = LogApi.get_by_id(login_api_id)
    try:
        delete_login_api(login_api_id)
        activity = f"DELETE {loginapi_data.login_api_name} from Login API Credentials."
        flash('Login API record deleted successfully', 'success')
    except Exception as e:
        activity = f"FAILED TO DELETE Login API Credentials due to error: {str(e)}."
        flash('An error occurred while deleting the record.', 'error')
    add_user_logs(activity)
    db.session.commit()
    return redirect(request.referrer)

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_email_api', methods=['POST'])#add email API credentials
@login_required
def register_email_api():
    try:
        new_ecredss = add_ecreds()  
        if new_ecredss:
            activity = f"ADDED {new_ecredss.ecreds_name} to Email API Credentials."
            flash('Email API credentials added successfully!', 'success')
        else:
            activity = f"FAILED TO ADD Email API Credentials. Missing or invalid data."
            flash('Failed to add Email API credentials.', 'error')
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD Email API Credentials due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))

@notifs.route('/edit_email_route/<int:ecreds_id>', methods=['POST'])#edit email API credentials
@login_required
def edit_email_route(ecreds_id):
    ecreds_data = Ecredss.get_by_id(ecreds_id)
    cur_name = ecreds_data.ecreds_name
    cur_email = ecreds_data.ecreds_email
    cur_sender = ecreds_data.ecreds_sender
    cur_password = ecreds_data.ecreds_password
    
    new_name = request.form.get('ecreds_name')
    new_email = request.form.get('ecreds_email')
    new_sender = request.form.get('ecreds_sender')
    new_password = request.form.get('ecreds_password')
    try:
        if edit_ecreds(ecreds_id):
            activity = f"EDIT Email API Credentials from: [{cur_name}, {cur_email}, {cur_sender}, {cur_password}]to [{new_name}, {new_email}, {new_sender}, {new_password}]."
            flash('Email API Credential updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT Email Credentials. Missing or invalid data."
            flash('Email API record not found or update failed', 'error')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EIDT Email API Credentials due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_email_route/<int:ecreds_id>', methods=['POST'])#delete email API credentials
@login_required
def delete_email_route(ecreds_id):
    ecreds_data = Ecredss.get_by_id(ecreds_id)
    try:
        delete_ecreds(ecreds_id)
        activity = f"DELETE {ecreds_data.ecreds_name} from Email API Credentials."
        flash('Email API record deleted successfully', 'success')
    except Exception as e:
        activity = f"FAILED TO DELETE Email API Credentials due to error: {str(e)}."
        flash('An error occurred while deleting the record.', 'error')
    add_user_logs(activity)
    db.session.commit()
    return redirect(request.referrer)

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_hrpears_api', methods=['POST'])#add hrpears API credentials
@login_required
def register_hrpears_api():
    try:
        new_hrpears = add_hrpears()  
        if new_hrpears:
            activity = f"ADDED {new_hrpears.hrpears_name} to Hrpears API Credentials."
            flash('Hrpears API credentials added successfully!', 'success')
        else:
            activity = f"FAILED TO ADD Hrpears API Credentials. Missing or invalid data."
            flash('Failed to add Hrpears API credentials.', 'error')
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD Hrpears API Credentials due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))

@notifs.route('/edit_hrpears_route/<int:hrpears_id>', methods=['POST'])#edit hrpears API credentials
@login_required
def edit_hrpears_route(hrpears_id):
    hrpears_data = Hrpears.get_by_id(hrpears_id)
    cur_host = hrpears_data.hrpears_host
    cur_root = hrpears_data.hrpears_root
    cur_user = hrpears_data.hrpears_user
    cur_password = hrpears_data.hrpears_password
    cur_dbname = hrpears_data.hrpears_dbname
    cur_table = hrpears_data.hrpears_table
    
    new_host = request.form.get('hrpears_host')
    new_root = request.form.get('hrpears_root')
    new_user = request.form.get('hrpears_user')
    new_password = request.form.get('hrpears_password')
    new_dbname = request.form.get('hrpears_dbname')
    new_table = request.form.get('hrpears_table')
    try:
        if edit_hrpears(hrpears_id):
            activity = f"EDIT HRpears API Credentials from: [{cur_host},{cur_root},{cur_user},{cur_password},{cur_dbname},{cur_table}]to [{new_host},{new_root},{new_user},{new_password},{new_dbname},{new_table}]."
            flash('HRpears API Credential updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT HRpears Credentials. Missing or invalid data."
            flash('HRpears API record not found or update failed', 'error')

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EDIT HRpears API Credentials due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_hrpears_route/<int:hrpears_id>', methods=['POST'])#delete hrpears API credentials
@login_required
def delete_hrpears_route(hrpears_id):
    hrpears_data = Hrpears.get_by_id(hrpears_id)
    try:
        delete_hrpears(hrpears_id)
        activity = f"DELETE {hrpears_data.hrpears_name} from HRpears API Credentials."
        flash('HRpears API record deleted successfully', 'success')
    except Exception as e:
        activity = f"FAILED TO DELETE HRpears API Credentials due to error: {str(e)}."
        flash('An error occurred while deleting the record.', 'error')
    add_user_logs(activity)
    db.session.commit()
    return redirect(request.referrer)

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_user', methods=['POST'])#add user
@login_required
def register_user():
    new_user = add_user()
    
    if not new_user:
        activity = f"FAILED TO ADD User Credentials. Missing or invalid data."
        add_user_logs(activity)
        db.session.commit()
        return redirect(url_for('notifs.admin'))
        
    try:
        role = Roles.get_by_id(new_user.role_id)
        activity = f"ADDED {new_user.full_name} as {role.role_name} to Users."
        flash('User Credentials added successfully!', 'success')
        add_user_logs(activity)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD User Credentials due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))
    
@notifs.route('/edit_user_route/<int:user_id>', methods=['POST'])#edit user
@login_required
def edit_user_route(user_id):
    user_data = User_v1.get_by_id(user_id)

    cur_fullname = user_data.full_name
    cur_username = user_data.username
    cur_role = user_data.role.role_name
    cur_division = user_data.division
    
    new_fullname = request.form.get('full_name')
    new_username = request.form.get('username')
    new_role_id = request.form.get('role_id')
    role_data = Roles.get_by_id(new_role_id)
    new_role = role_data.role_name
    new_division = request.form.get('division')
    
    try:
        if edit_user(user_id):
            activity = f"EDIT User data from: [{cur_fullname}, {cur_username}, {cur_role}, {cur_division}] to [{new_fullname}, {new_username}, {new_role}, {new_division}]."
            flash('User data updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT User data. Missing or invalid data."

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EDIT User data due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_user_route/<int:user_id>', methods=['POST'])#delete user
@login_required
def delete_user_route(user_id):
    user_data = User_v1.get_by_id(user_id)
    if not user_data:
        flash('User not found.', 'error')
        return redirect(url_for('notifs.admin'))
    success = delete_user(user_id)
    if success:
        flash('User record deleted successfully', 'success')
        activity = f"DELETED {user_data.full_name} from Users data."
    else:
        flash('User record delete failed', 'error')
        activity = f"FAILED TO DELETE {user_data.full_name} from Users data."
    
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_role', methods=['POST'])#add user type
@login_required
def register_role():
    new_roles = add_role()
    
    if not new_roles:
        activity = f"FAILED TO ADD User type due Missing or invalid data."
        add_user_logs(activity)
        db.session.commit()
        return redirect(url_for('notifs.admin'))
        
    try:
        activity = f"ADDED {new_roles.role_name} as User types."
        flash('User type added successfully!', 'success')
        add_user_logs(activity)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD User type due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))
    
@notifs.route('/edit_role_route/<int:role_id>', methods=['POST'])#edit user type
@login_required
def edit_role_route(role_id):
    role_data = Roles.get_by_id(role_id)
    cur_type = role_data.role_name
    cur_description = role_data.role_description
    new_type = request.form.get('role_name')
    new_description = request.form.get('role_description')

    try:
        if edit_role(role_id):
            activity = f"EDIT User Type from: [{cur_type}, {cur_description}] to [{new_type}, {new_description}]."
            flash('User type updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT User type. Missing or invalid data."
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EDIT User type due to error: {str(e)}."

    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_role_route/<int:role_id>', methods=['POST'])#delete user type
@login_required
def delete_role_route(role_id):
    role_data = Roles.get_by_id(role_id)
    if not role_data:
        flash('User not found.', 'error')
        return redirect(url_for('notifs.admin'))
    success = delete_role(role_id)
    if success:
        flash('User type record deleted successfully', 'success')
        activity = f"DELETED {role_data.role_name} from User types."
    else:
        flash('User type record delete failed', 'error')
        activity = f"FAILED TO DELETE {role_data.role_name} from User types."
    
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

#----------------------------------------------------------------------------------------------------------->
@notifs.route('/register_division', methods=['POST'])#add user division
@login_required
def register_division():
    new_division = add_division()
    
    if not new_division:
        activity = f"FAILED TO ADD Division due Missing or invalid data."
        add_user_logs(activity)
        db.session.commit()
        return redirect(url_for('notifs.admin'))
        
    try:
        activity = f"ADDED {new_division.division_name} as User Division."
        flash('User type added successfully!', 'success')
        add_user_logs(activity)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD User type due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.admin'))
    
@notifs.route('/edit_division_route/<int:division_id>', methods=['POST'])#edit user division
@login_required
def edit_division_route(division_id):
    division_data = Divisions.get_by_id(division_id)
    cur_division = division_data.division_name
    cur_description = division_data.division_description
    new_division = request.form.get('division_name')
    new_description = request.form.get('division_description')
    
    try:
        if edit_division(division_id):
            activity = f"EDIT User division from: [{cur_division}, {cur_description}] to [{new_division}, {new_description}]."
            flash('User division updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT User division. Missing or invalid data."
   
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EDIT User division due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_division_route/<int:division_id>', methods=['POST'])#delete user division
@login_required
def delete_division_route(division_id):
    division_data = Divisions.get_by_id(division_id)
    if not division_data:
        flash('User division not found.', 'error')
        return redirect(url_for('notifs.admin'))
    success = delete_division(division_id)
    if success:
        flash('User division record deleted successfully', 'success')
        activity = f"DELETED {division_data.division_name} from User divisions."
    else:
        flash('User division record delete failed', 'error')
        activity = f"FAILED TO DELETE {division_data.division_name} from User divisions."
    
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))

@notifs.route('/delete_logs_route/<int:log_id>', methods=['POST'])#delete user logs
@login_required
def delete_logs_route(log_id):
    log_data = User_logs.get_by_id(log_id)
    if not log_data:
        flash('User division not found.', 'error')
        return redirect(url_for('notifs.admin'))
    flash('User logs record deleted successfully', 'success')
    delete_user_logs(log_id)
    return redirect(url_for('notifs.admin'))

#===============================================================================================================================>
#
#
#
#================ Home =========================================================================================================>
@notifs.route('/', methods=['GET', 'POST'])#Home page
@login_required
def home():
    msg_data = Msg_log.query.filter_by(msg_sender=current_user.full_name).all()
    total_sent = sum(1 for msg in msg_data if msg.msg_status == 'sent')
    total_unsent = sum(1 for msg in msg_data if msg.msg_status == 'unsent')

    theme_data = Theme.get_all()

    return render_template("index.html",
                           theme_data=theme_data,
                           msg_data=msg_data,
                           total_sent=total_sent,
                           total_unsent=total_unsent)

@notifs.route('/display_data', methods=['GET', 'POST'])#Display Internal data from HRIS to directory
@login_required
def display_data():
    
    data = get_table_data()
    if data:
        return jsonify(data)
    else:
        flash('Cannot connect to server.', 'error')

@notifs.route('/display_external_data', methods=['GET', 'POST'])#Display External data from local database to directory
@login_required
def display_external_data():
    data = External.get_all()
    if data:
        return jsonify([
            {
                'name': item.external_name,
                'mobile_no': item.external_mobile,
                'email': item.external_email
            } 
            for item in data
        ])
    else:
        flash('Cannot connect to database.', 'error')

@notifs.route('/select_theme/<int:theme_id>', methods=['POST'])#Select theme
@login_required
def select_theme(theme_id):
    try:
        user_id = current_user.user_id
        user_theme = User_v1.get_by_id(user_id)
        user_theme.theme_id = theme_id
        db.session.commit()

        flash('Successfully changed theme, refresh or re-login if theme does not take effect.', 'success')
        return redirect(url_for('notifs.home'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error on changing theme: {str(e)}', 'error')
        return redirect(url_for('notifs.home'))

@notifs.route('/delete_msglogs_route/<int:msg_id>', methods=['POST'])#delete message logs
@login_required
def delete_msglogs_route(msg_id):
    msglog_data = Msg_log.get_by_id(msg_id)
    if not msglog_data:
        flash('User division not found.', 'error')
        return redirect(url_for('notifs.home'))
    success = delete_msg_log(msg_id)
    msg_sender = msglog_data.msg_sender
    sent_on = msglog_data.sent_on
    msg_content = msglog_data.msg_content
    credit_used = msglog_data.credit_used
    msg_recipient = msglog_data.msg_recipient
    
    if success:
        flash('Message Log deleted successfully', 'success')
        activity = f"DELETED {credit_used} Credit/s Message/s:{msg_content} sent to {msg_recipient} on {sent_on}| Sender: {msg_sender}."
    else:
        flash('Message Log delete failed', 'error')
        activity = f"DELETED {credit_used} Credit/s Message/s:{msg_content} sent to {msg_recipient} on {sent_on}| Sender: {msg_sender}."
    
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.home'))

@notifs.route('/send_single_msg', methods=['POST'])#Send single message
@login_required
def send_single_msg():
    sent=[]
    unsent=[]
    msg_recipient=[]
    total_credit=0
    
    sender_div = current_user.division

    sender = request.form.get('sender')
    sending_option = request.form.get('sending_option')

    recipient = request.form.get('recipient')
    formatted_name = extract_first_name(recipient)
    content = request.form.get('message')
    
    add_name = request.form.get('addName')

    msg_tracker = generate_tracker(sender_div,sending_option)
    
    message = message_content(add_name,formatted_name,content,sender,sender_div)
    if sending_option == 'sms':
        mobile = request.form.get('phone')
        formatted_mobile = format_mobile_number(mobile)
        status_data = get_status_data(recipient,formatted_mobile,message)
        url, payload, headers = send_msg(message, formatted_mobile)
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            credit_used = int(data.get('TotalCreditUsed', 0))
            total_credit += int(credit_used)
            sent.append(status_data)
        else:
            unsent.append(status_data)

    elif sending_option == 'email':
        email = request.form.get('email')
        formatted_email = format_email(email)
        flash(f'email: {formatted_email}','error')
        
    else:
        recipient_contact = "none"
        
    total_sent = len(sent)
    total_unsent = len(unsent)
    msg_sent_str = json.dumps(sent) if isinstance(sent, list) else str(sent)
    msg_unsent_str = json.dumps(unsent) if isinstance(unsent, list) else str(unsent)
    msg_recipient_str = json.dumps(msg_recipient)
    
    if total_unsent == 0 and total_sent == 0:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        flash(f'{msg_status}','success')
    else:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        flash(f'{msg_status}','error')

    add_msg_log(msg_tracker, sending_option, msg_recipient_str, content, msg_status, msg_sent_str, msg_unsent_str, total_credit)
    return redirect(url_for('notifs.home'))

@notifs.route('/send_multi_msg', methods=['POST'])#Send Multi message
@login_required
def send_multi_msg():
    sender_div = current_user.division
    sender = request.form.get('msender')
    sending_option = request.form.get('msending_option')
    content = request.form.get('mmessage') 
    add_name = request.form.get('maddName')
    
    data = request.form.get('mlist')
    data_lines = data.strip().split("\n")
    
    msg_tracker = generate_tracker(sender_div,sending_option)
    
    sent=[]
    unsent=[]
    msg_recipient=[]
    total_credit=0
    
    for data_line in data_lines:
        data_parts = data_line.split(":")
        name = data_parts[0].strip()
        mobile = data_parts[1].strip()
        email = data_parts[2].strip()
        formatted_name = extract_first_name(name)
        formatted_mobile = format_mobile_number(mobile)
        formatted_email = format_email(email)
        message = message_content(add_name,formatted_name,content,sender,sender_div)
        status_data = get_status_data(name,formatted_mobile,message)
        recipient =f"{name}:{formatted_mobile}"
        msg_recipient.append(recipient)
        
        if sending_option == 'sms':
            url, payload, headers = send_msg(message, formatted_mobile)
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 200:
                credit_used = int(data.get('TotalCreditUsed', 0))
                total_credit += int(credit_used)
                sent.append(status_data)
            else:
                unsent.append(status_data)
        elif sending_option == 'email':
            flash(f'email: {formatted_email}','error')

    total_sent = len(sent)
    total_unsent = len(unsent)
    msg_sent_str = json.dumps(sent) if isinstance(sent, list) else str(sent)
    msg_unsent_str = json.dumps(unsent) if isinstance(unsent, list) else str(unsent)
    msg_recipient_str = json.dumps(msg_recipient)
    
    if total_unsent == 0 and total_sent == 0:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        flash(f'{msg_status}','success')
    else:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        flash(f'{msg_status}','error')

    add_msg_log(msg_tracker, sending_option, msg_recipient_str, content, msg_status, msg_sent_str, msg_unsent_str, total_credit)
    return redirect(url_for('notifs.home'))


        
        
        
        
        
        
    























#===============================================================================================================================>
#
#
#
#================ Libraries ====================================================================================================>
@notifs.route('/libraries', methods=['GET', 'POST'])
@login_required
def libraries():
    return render_template('libraries.html')

#===============================================================================================================================>
#
#
#
#================ Reports ======================================================================================================>
@notifs.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    return render_template('reports.html')

#===============================================================================================================================>
#
#
#
#================ Profile ======================================================================================================>
@notifs.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')
#===============================================================================================================================>