#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
#flask / requirements libraries
import json
import pymysql
import requests
from flask_migrate import Migrate
from config import Config
from io import StringIO
from collections import defaultdict
from extensions import db, limiter
from flask import Blueprint, request, render_template, redirect, url_for, session, flash, jsonify, g
from flask_login import login_required, logout_user
from flask_login import login_user, current_user
#===============================================================================================================================>
#Utils
from utility.sys_utils import get_manila_time, get_login_data, encrypt_content, decrypt_content
from utility.msg_utils import message_content, chunk_contents, generate_tracker, get_status_data,send_msg2, send_msg, get_hrpears_data, get_eprocsys_data, convert_file_to_inputs, sms_API_credits_checker, multi_recipient_proccessor
from utility.format_utils import extract_first_name, format_mobile_number, format_email, format_amount
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
from models.message_temp import Msg_templates
#===============================================================================================================================>
#Controllers
from controllers.user_role import add_role, edit_role, delete_role
from controllers.user import add_user, edit_user, delete_user, edit_credit_used, edit_user_notes
from controllers.user_logs import add_user_logs, delete_user_logs
from controllers.user_division import add_division, edit_division, delete_division, edit_division_credit_used
from controllers.external_contacts import add_external, edit_external, delete_external
from controllers.login_credentials import add_login_api, edit_login_api, delete_login_api
from controllers.user_themes import add_theme, edit_theme, delete_theme
from controllers.itexmo_credentials import add_itexmo, edit_itexmo, delete_itexmo, credits_check
from controllers.email_credentials import add_ecreds, delete_ecreds, edit_ecreds
from controllers.hrpears_credentials import add_hrpears, edit_hrpears, delete_hrpears
from controllers.system_settings import edit_sys_setting, edit_system_notice
from controllers.msg_log import add_msg_log, delete_msg_log
from controllers.message_temp import add_msg_temp, edit_msg_temp, delete_msg_temp
#===============================================================================================================================>
notifs = Blueprint('notifs', __name__, template_folder='templates')
#===============================================================================================================================>
#===============================================================================================================================>
#
#
@notifs.route("/ping")
def ping():
    return "pong", 200
#
#===============================================================================================================================>
#================ System Settings ==============================================================================================>
    #system settings page
@notifs.route('/system_settings/<int:sys_setting_id>', methods=['GET', 'POST'])
@login_required
def system_settings(sys_setting_id):
    sys_settings_data = SysSettings.get_by_id(sys_setting_id)
    itexmo_data = Itexmo.get_all()
    email_data = Ecredss.get_all()
    hrpears_data = Hrpears.get_all()
    login_data = LogApi.get_all()
    return render_template('admin_modals/system_settings.html',
                           sys_settings_data=sys_settings_data,
                           itexmo_data=itexmo_data,
                           email_data=email_data,
                           hrpears_data=hrpears_data,
                           login_data=login_data)
#===============================================================================================================================>
#===============================================================================================================================>
#
#
#
#===============================================================================================================================>
#================ Admin ========================================================================================================>
    #Admin page
@notifs.route('/admin', methods=['GET', 'POST'])
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
    decrypted_users = []
    for u in user_data:
        decrypted_users.append({
            "user_id":u.user_id,
            "username":u.username,
            "full_name":decrypt_content(u.full_name),
            "user_email":u.user_email,
            "division":u.division,
            "user_section":u.user_section,
            "role_id":u.role_id,
            "theme_id":u.theme_id,
            "login_status":u.login_status,
            "cur_login":u.cur_login,
            "last_login":u.last_login,
            "last_logout":u.last_logout,
            "user_notes":u.user_notes,
            "msg_sent":u.msg_sent,
            "credit_used":u.credit_used,
            "created_by":u.created_by,
            "created_on":u.created_on,
            "updated_by":u.updated_by,
            "updated_on":u.updated_on,
            "created_at":u.created_at,
            "updated_at":u.updated_at,
            "role":u.role,
            "theme":u.theme  
        })
      
    total_user = len(user_data)
    
    role_data = Roles.get_all()
    total_role = len(role_data)
    
    division_data = Divisions.get_all()
    total_division = len(division_data)
    
    log_data = User_logs.get_all()
    decrypted_logs = []
    for logs in log_data:
        decrypted_logs.append({
            "log_id": logs.log_id,
            "user": decrypt_content(logs.user),
            "activity": logs.activity,
            "created_on": logs.created_on     
        })
    total_log = len(log_data)
    
    msglog_data = Msg_log.get_all()
    decrypted_msglogs = []
    for msglogs in msglog_data:
        raw_recipients = msglogs.msg_recipient
        recipient_list = [r.strip() for r in raw_recipients.split(",") if r.strip()]
        recipient_count = len(recipient_list)
        decrypted_msglogs.append({
            "msg_id": msglogs.msg_id,
            "msg_tracker": msglogs.msg_tracker,
            "msg_type": msglogs.msg_type,
            "msg_sender": decrypt_content(msglogs.msg_sender),
            "msg_division": msglogs.msg_division,
            "recipient_count": recipient_count,
            "credit_used": msglogs.credit_used,
            "sent_on": msglogs.sent_on,    
        })
    total_log = len(log_data)
    
    sys_settings_data = SysSettings.get_by_id(1)
    
    return render_template('admin_modals/admin.html',
                           role_data=role_data,
                           total_role=total_role,
                           user_data=decrypted_users,
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
                           log_data=decrypted_logs,
                           total_log=total_log,
                           sys_settings_data=sys_settings_data)
#===========================================================================================================>
    #System settings
@notifs.route('/edit_system_settings_route/<int:sys_setting_id>', methods=['POST'])
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
#===========================================================================================================>
    #Login
@notifs.route('/login', methods=['GET', 'POST'])
# @limiter.limit("5 per minute")
def login():

    if current_user.is_authenticated:
        return redirect(url_for('notifs.home'))
    
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
                user_status = user.login_status
                if user_status == 1:
                    flash('User account already logged in', 'error')
                    return render_template('login.html')
                    
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
                    user_status = user.login_status

                    login_user(user)
                    response_data = response.json()
                    email = response_data['data']['email']
                    division = response_data['data']['division']
                    section = response_data['data']['section']

                    user.cur_login = get_manila_time()
                    user.user_email = encrypt_content(email)
                    user.division = division
                    user.user_section = section
                    user.login_status = 1 
                    
                    db.session.commit()
                    flash('Login successful!', 'success')
                    return redirect(url_for('notifs.home'))
                else:
                    flash('Invalid username or password', 'error')
            else:
                flash('Sorry you are not granted access to NotifX', 'error')
        return render_template('login.html')

    except requests.exceptions.RequestException:
        flash('There was an issue with the login request.', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    return render_template('login.html')
#===========================================================================================================>
    #Logout
@notifs.route('/logout')
@login_required
def logout():
    current_user.last_logout = get_manila_time()
    login_session = current_user.cur_login
    if login_session:
        current_user.last_login = current_user.cur_login
    else:
        current_user.last_login = get_manila_time()
    current_user.login_status = 0
    
    db.session.commit()
    session.clear()
    
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('notifs.login'))
#===========================================================================================================>
                            #ITEXMO API CREDENTIALS
#===========================================================================================================>
    #add itexmo credentials
@notifs.route('/register_itexmo', methods=['POST'])
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
#===========================================================================================================>
    #edit itexmo credentials
@notifs.route('/edit_itexmo_route/<int:itexmo_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete itexmo credentials
@notifs.route('/delete_itexmo/<int:itexmo_id>', methods=['POST'])
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
#===========================================================================================================>
                            #LOGIN API CREDENTIALS
#===========================================================================================================>
    #add login API credentials
@notifs.route('/register_login_api', methods=['POST'])
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
#===========================================================================================================>
    #edit login API credentials
@notifs.route('/edit_loginapi_route/<int:login_api_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete login API credentials
@notifs.route('/delete_loginapi_route/<int:login_api_id>', methods=['POST'])
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
#===========================================================================================================>
                            #EMAIL API CREDENTIALS
#===========================================================================================================>
    #add email API credentials
@notifs.route('/register_email_api', methods=['POST'])
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
#===========================================================================================================>
    #edit email API credentials
@notifs.route('/edit_email_route/<int:ecreds_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete email API credentials
@notifs.route('/delete_email_route/<int:ecreds_id>', methods=['POST'])
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
#===========================================================================================================>
                            #HRIS DATABASE CREDENTIALS
#===========================================================================================================>
    #add hrpears API credentials
@notifs.route('/register_hrpears_api', methods=['POST'])
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
#===========================================================================================================>
    #edit hrpears API credentials
@notifs.route('/edit_hrpears_route/<int:hrpears_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete hrpears API credentials
@notifs.route('/delete_hrpears_route/<int:hrpears_id>', methods=['POST'])
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
#===========================================================================================================>
                            #APP USERS
#===========================================================================================================>
    #Display login data from HRIS to directory
@notifs.route('/display_users_data', methods=['GET', 'POST'])
@login_required
def display_users_data():
    
    data = get_login_data()
    if data:
        return jsonify(data)
    else:
        flash('Cannot connect to server.', 'error')
#===========================================================================================================>
    #add user
@notifs.route('/register_user', methods=['POST'])
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
        decrepted_new_user = decrypt_content(new_user.full_name)
        activity = f"ADDED {decrepted_new_user} as {role.role_name} to Users."
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
#===========================================================================================================>
    #edit user
@notifs.route('/edit_user_route/<int:user_id>', methods=['POST'])
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
    decrypted_cur_fullname = decrypt_content(cur_fullname)
    
    try:
        if edit_user(user_id):
            activity = f"EDIT User data from: [{decrypted_cur_fullname}, {cur_username}, {cur_role}, {cur_division}] to [{new_fullname}, {new_username}, {new_role}, {new_division}]."
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
#===========================================================================================================>
    #delete user
@notifs.route('/delete_user_route/<int:user_id>', methods=['POST'])
@login_required
def delete_user_route(user_id):
    user_data = User_v1.get_by_id(user_id)
    decrypted_fullname = decrypt_content(user_data.full_name)
    if not user_data:
        flash('User not found.', 'error')
        return redirect(url_for('notifs.admin'))
    success = delete_user(user_id)
    if success:
        flash('User record deleted successfully', 'success')
        activity = f"DELETED {decrypted_fullname} from Users data."
    else:
        flash('User record delete failed', 'error')
        activity = f"FAILED TO DELETE {decrypted_fullname} from Users data."
    
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.admin'))
#===========================================================================================================>
                            #APP USERS ROLES/TYPES
#===========================================================================================================>
    #add user type/role
@notifs.route('/register_role', methods=['POST'])
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
#===========================================================================================================>
    #edit user type/role
@notifs.route('/edit_role_route/<int:role_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete user type/role
@notifs.route('/delete_role_route/<int:role_id>', methods=['POST'])
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
#===========================================================================================================>
                            #APP USERS DIVISIONS
#===========================================================================================================>
    #add user division
@notifs.route('/register_division', methods=['POST'])
@login_required
def register_division():
    new_division = add_division()
    
    if not new_division:
        
        activity = f"FAILED TO ADD Division due Missing or invalid data."
        add_user_logs(activity)
        db.session.commit()
        return redirect_based_on_role()
        
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
    return redirect_based_on_role()

def redirect_based_on_role():
    if current_user.role_id == 1:
        return redirect(url_for('notifs.admin'))
    else:
        return redirect(url_for('notifs.home'))
#===========================================================================================================>
    #edit user division
@notifs.route('/edit_division_route/<int:division_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete user division
@notifs.route('/delete_division_route/<int:division_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete user logs
@notifs.route('/delete_logs_route/<int:log_id>', methods=['POST'])
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
#===============================================================================================================================>
#
#
#
#===============================================================================================================================>
#================ Home =========================================================================================================>
    #Home page
@notifs.route('/', methods=['GET', 'POST'])
@login_required
def home():
    decrypted_name = decrypt_content(current_user.full_name)
    name_parts = decrypted_name.split(' ')
    first_name = name_parts[0].title()
    last_name = name_parts[1].title() if len(name_parts) > 1 and '.' not in name_parts[1] else ''
    
    msg_data = Msg_log.query.filter_by(msg_sender=current_user.full_name).all()
    emails = Msg_log.query.filter_by(msg_sender=current_user.full_name, msg_type="email").all()
    smss = Msg_log.query.filter_by(msg_sender=current_user.full_name, msg_type="sms").all()
    
    emails_sent = len(emails)
    sms_sent = len(smss)
  
    
    theme_data = Theme.get_all()
    msg_temp_data = Msg_templates.get_all()
    division_data = Divisions.get_all()

    return render_template("home_modals/index.html",
                           theme_data=theme_data,
                           emails=emails,
                           smss=smss,
                           emails_sent=emails_sent,
                           sms_sent=sms_sent,
                           msg_temp_data=msg_temp_data,
                           msg_data=msg_data,
                           division_data=division_data,
                           first_name=first_name,
                           last_name=last_name)
#===========================================================================================================>
    #User Notes
@notifs.route('/edit_user_notes_route/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user_notes_route(user_id):
    try:
        if edit_user_notes(user_id):
            flash('Notes added successfully', 'success')
        else:
            flash('Error on adding notes', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
    return redirect(url_for('notifs.home'))
#===========================================================================================================>
    #System Notes
@notifs.route('/edit_system_notice_route/<int:sys_setting_id>', methods=['GET', 'POST'])
@login_required
def edit_system_notice_route(sys_setting_id):
    try:
        if edit_system_notice(sys_setting_id):
            flash('System Notice added successfully', 'success')
        else:
            flash('Error on adding System Notice ', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
    return redirect(url_for('notifs.home'))
#===========================================================================================================>
    #Select theme
@notifs.route('/select_theme/<int:theme_id>', methods=['POST'])
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
#===========================================================================================================>
    #delete message logs
@notifs.route('/delete_msglogs_route/<int:msg_id>', methods=['POST'])
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
#===========================================================================================================>
                            #MESSAGE SENDER DIRECTORY
#===========================================================================================================>
    #Display Internal data from HRIS to directory
@notifs.route('/display_hrpears_data', methods=['GET', 'POST'])
@login_required
def display_hrpears_data():
    
    data = get_hrpears_data()
    if data:
        return jsonify(data)
    else:
        flash('Cannot connect to server.', 'error')
#===========================================================================================================>
    #Display Supplier data from e procsys to directory
@notifs.route('/display_eprocsys_data', methods=['GET', 'POST'])
@login_required
def display_eprocsys_data():
    
    data = get_eprocsys_data()
    if data:
        return jsonify(data)
    else:
        flash('Cannot connect to server.', 'error')
#===========================================================================================================>
                            #MESSAGE SENDER FORM
#===========================================================================================================>
    #Send single message
@notifs.route('/send_single_msg', methods=['POST'])
@login_required
def send_single_msg():
    user_data = User_v1.get_by_id(current_user.user_id)
    user_credit = user_data.credit_used
    sent=[]
    unsent=[]
    msg_recipient=[]
    total_credit=0
    
    sender_div = current_user.division
    division = int(request.form.get('sdvision'))
    
    divsion_data = Divisions.get_by_id(division)
    division_credit = divsion_data.division_credits
    msg_division = divsion_data.division_name
    
    sender = request.form.get('sender')
    sending_option = request.form.get('sending_option')
    recipient = request.form.get('recipient')
    formatted_name = extract_first_name(recipient)
    content = request.form.get('message')

    add_name = request.form.get('addName')
    msg_tracker = generate_tracker(msg_division,sending_option)
    
    
    message = message_content(add_name,formatted_name,content,sender,sender_div)
    if sending_option == 'sms':
        mobile = request.form.get('phone')
        formatted_mobile = format_mobile_number(mobile)
        status_data = get_status_data(recipient,formatted_mobile,message)
        formatted_recipient =f"{recipient}:{formatted_mobile}"
        msg_recipient.append(formatted_recipient)
        
        url, payload, headers = send_msg(message, formatted_mobile)
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            credit_used = int(data.get('TotalCreditUsed', 0))
            total_credit += int(credit_used)
            sent.append(status_data)
            sms_API_credits_checker()
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
    msg_sent_str = json.dumps(sent, ensure_ascii=False) if sent else ""
    msg_unsent_str = json.dumps(unsent, ensure_ascii=False) if unsent else ""
    msg_recipient_str = json.dumps(msg_recipient, ensure_ascii=False)
    
    if total_unsent == 0:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        # flash(f'{msg_status}','success')
    else:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        # flash(f'{msg_status}','error')

    add_msg_log(msg_tracker, sending_option, msg_recipient_str, content, msg_status, msg_division, msg_sent_str, msg_unsent_str, total_credit)
    user_credit+=total_credit
    division_credit+=total_credit
    edit_credit_used(current_user.user_id, user_credit)
    edit_division_credit_used(division, division_credit)
    return redirect(url_for('notifs.home',total_sent=total_sent, total_unsent=total_unsent ))
#===========================================================================================================>
    #Send Multi message
@notifs.route('/send_multi_msg', methods=['POST'])
@login_required
def send_multi_msg():
    user_data = User_v1.get_by_id(current_user.user_id)
    user_credit = user_data.credit_used
    sender_div = current_user.division
    
    division = int(request.form.get('mdvision'))
    
    divsion_data = Divisions.get_by_id(division)
    division_credit = divsion_data.division_credits
    msg_division = divsion_data.division_name
    
    sender = request.form.get('msender')
    sending_option = request.form.get('msending_option')
    content = request.form.get('mmessage') 
    add_name = request.form.get('maddName')
    
    data = request.form.get('mlist')
    data_lines = data.strip().split("\n")
    
    msg_tracker = generate_tracker(msg_division,sending_option)
    
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
                sms_API_credits_checker()
            else:
                unsent.append(status_data)
        elif sending_option == 'email':
            flash(f'email: {formatted_email}','error')

    total_sent = len(sent)
    total_unsent = len(unsent)
    msg_sent_str = json.dumps(sent, ensure_ascii=False) if sent else ""
    msg_unsent_str = json.dumps(unsent, ensure_ascii=False) if unsent else ""
    msg_recipient_str = json.dumps(msg_recipient, ensure_ascii=False)
    
    
    if total_unsent == 0:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        # flash(f'{msg_status}','success')
    else:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        # flash(f'{msg_status}','error')

    add_msg_log(msg_tracker, sending_option, msg_recipient_str, content, msg_status,msg_division, msg_sent_str, msg_unsent_str, total_credit)
    user_credit+=total_credit
    edit_credit_used(current_user.user_id, user_credit)
    division_credit+=total_credit
    edit_division_credit_used(division, division_credit)
    return redirect(url_for('notifs.home', total_sent=total_sent, total_unsent=total_unsent))
#===========================================================================================================>
    #Generate recipient from upload
@notifs.route('/generate_from_upload', methods=['POST'])
@login_required
def generate_from_upload():
    file = request.files.get('uploaded')
    if not file:
        print("No file uploaded")
        return redirect(url_for('notifs.home'))
    matched_records, not_found = convert_file_to_inputs(file)

    return {
        "matched_records": matched_records if matched_records else ["No data found"],
        "unmatched_names": not_found if not_found else ["All data are found"]
    }
#===========================================================================================================>
    #Send Upload message
@notifs.route('/send_upload_msg', methods=['POST'])
@login_required
def send_upload_msg():
    user_data = User_v1.get_by_id(current_user.user_id)
    user_credit = user_data.credit_used
    sender_div = current_user.division
    division = int(request.form.get('udvision'))
    divsion_data = Divisions.get_by_id(division)
    division_credit = divsion_data.division_credits
    msg_division = divsion_data.division_name
    sender = request.form.get('usender')
    sending_option = request.form.get('usending_option')
    content = request.form.get('umessage')
    add_name = request.form.get('uaddName')
    data = request.form.get('ufounddata')
    if data == "No data found":
        flash("","error")
        return redirect(url_for('notifs.home'))
    msg_tracker = generate_tracker(msg_division,sending_option)
    total_credit=0
    sent =0
    unsent =0
    if sending_option == 'sms':
        contents , msg_recipient, formatted_email, total_contents  = multi_recipient_proccessor(data, add_name, content, sender, sender_div)
        chunks = chunk_contents(contents, 250)
        for chunk in chunks:
            url, payload, headers = send_msg2(chunk)
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                response_data = response.json()
                print(response_data)
            except requests.RequestException as e:
                flash(f"[ERROR] Failed to send: {e}")
                continue
            if response.status_code == 200:
                credit_used = int(response_data.get('TotalCreditUsed', 0))
                accepted = int(response_data.get('Accepted', 0))
                failed = int(response_data.get('Failed', 0))
                total_credit += int(credit_used)
                sent += int(accepted)
                unsent += int(failed)
                sms_API_credits_checker()
    elif sending_option == 'email':
        flash(f'email: {formatted_email}','error')
    total_sent = sent
    total_unsent = unsent
    msg_sent_str = json.dumps(sent, ensure_ascii=False) if sent else ""
    msg_unsent_str = json.dumps(unsent, ensure_ascii=False) if unsent else ""
    msg_recipient_str = json.dumps(msg_recipient, ensure_ascii=False)
    if total_unsent == 0:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        # flash(f'{msg_status}','success')
    else:
        msg_status = f"Sent: {total_sent}, Unsent: {total_unsent}" 
        # flash(f'{msg_status}','error')
    add_msg_log(msg_tracker, sending_option, msg_recipient_str, content, msg_status, msg_division, msg_sent_str, msg_unsent_str, total_credit)
    user_credit+=total_credit
    edit_credit_used(current_user.user_id, user_credit)
    division_credit+=total_credit
    edit_division_credit_used(division, division_credit)
    return redirect(url_for('notifs.home', total_sent=total_sent, total_unsent=total_unsent, total_contents=total_contents ))
#===========================================================================================================>
                            #MESSAGE TEMPLATES
#===========================================================================================================>
    #Add message template
@notifs.route('/register_msg_temp', methods=['POST'])
@login_required
def register_msg_temp():
    new_msg_temp = add_msg_temp()
    
    if not new_msg_temp:
        activity = f"FAILED TO ADD Message template due Missing or invalid data."
        add_user_logs(activity)
        db.session.commit()
        return redirect(url_for('notifs.home'))
        
    try:
        activity = f"ADDED {new_msg_temp.msg_temp_name} as Message template."
        flash('Message template added successfully!', 'success')
        add_user_logs(activity)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD Message template due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('notifs.home'))
#===========================================================================================================>
    #edit Message template
@notifs.route('/edit_msg_temp_route/<int:msg_temp_id>', methods=['POST'])
@login_required
def edit_msg_temp_route(msg_temp_id):
    msg_temp_data = Msg_templates.get_by_id(msg_temp_id)
    cur_msg_temp = msg_temp_data.msg_temp_name
    cur_msg_temp_description = msg_temp_data.msg_temp_description
    new_msg_temp = request.form.get('msg_temp_name')
    new_msg_temp_description = request.form.get('msg_temp_description')
    
    try:
        if edit_msg_temp(msg_temp_id):
            activity = f"EDIT Message template from: [{cur_msg_temp}, {cur_msg_temp_description}] to [{new_msg_temp}, {new_msg_temp_description}]."
            flash('User division updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT Message template. Missing or invalid data."
   
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback() 
        activity = f"FAILED TO EDIT Message template due to error: {str(e)}."
        
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.home'))
#===========================================================================================================>
    #delete Message template
@notifs.route('/delete_msg_temp_route/<int:msg_temp_id>', methods=['POST'])
@login_required
def delete_msg_temp_route(msg_temp_id):
    msg_temp_data = Msg_templates.get_by_id(msg_temp_id)
    if not msg_temp_data:
        flash('Message template not found.', 'error')
        return redirect(url_for('notifs.admin'))
    success = delete_msg_temp(msg_temp_id)
    if success:
        flash('Message template record deleted successfully', 'success')
        activity = f"DELETED {msg_temp_data.msg_temp_name} from Message template."
    else:
        flash('Message template record delete failed', 'error')
        activity = f"FAILED TO DELETE {msg_temp_data.msg_temp_name} from Message template."
    
    add_user_logs(activity)
    db.session.commit()
    return redirect(url_for('notifs.home'))

#===========================================================================================================>
#===========================================================================================================>



















#===============================================================================================================================>
#
#
#
#
#
#================ Reports =====================================================================================================>
@notifs.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    sms_id = g.sys_settings.msg_api_id if g.sys_settings and g.sys_settings.msg_api_id else 1
    api_data = Itexmo.get_by_id(sms_id)
    user_credit = current_user.credit_used
    total_credits_remaining = api_data.credits_remaining
    total_credits_used = api_data.credits_consumed
    
    user_data = User_v1.get_all()
    
    total_credit_used = sum(user.credit_used for user in user_data)
    
    division_data = {}
    for user in user_data:
        division_data[user.division] = division_data.get(user.division, 0) + user.credit_used
        
    div_data= Divisions.get_all()
    
    division_creds_data = {}
    for division in div_data:
        division_creds_data[division.division_name] = division_creds_data.get(division.division_name, 0) + division.division_credits
        

    return render_template('reports.html',
                           user_credit=user_credit,
                           total_credit_used=total_credit_used,
                           total_credits_remaining=total_credits_remaining,
                           total_credits_used=total_credits_used,
                           division_data=division_data,
                           division_creds_data=division_creds_data)





#===============================================================================================================================>
#
#
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
#
#
#================ Profile ======================================================================================================>
@notifs.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')
#===============================================================================================================================>
#===============================================================================================================================>



