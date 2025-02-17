from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import login_required, logout_user
from flask_migrate import Migrate
from config import Config
from flask_login import login_user, current_user
from utils import get_manila_time
import requests
from extensions import db

#Models
from models.user import User_v1
from models.user_role import Roles
from models.user_logs import User_logs
from models.user_division import Divisions
from models.external_credentials import External
from models.login_credentials import LogApi
from models.user_themes import Theme
from models.itexmo_credentials import Itexmo
from models.email_credentials import Ecredss
from models.hrpears_credentials import Hrpears

#Controllers
from controllers.user_role import add_role, edit_role, delete_role
from controllers.user import add_user, edit_user, delete_user, change_theme
from controllers.user_logs import add_user_logs, delete_user_logs
from controllers.user_division import add_division, edit_division, delete_division
from controllers.external_credentials import add_external, edit_external, delete_external
from controllers.login_credentials import add_login_api, edit_login_api, delete_login_api
from controllers.user_themes import add_theme, edit_theme, delete_theme
from controllers.itexmo_credentials import add_itexmo, edit_itexmo, delete_itexmo
from controllers.email_credentials import add_ecreds, delete_ecreds, edit_ecreds
from controllers.hrpears_credentials import add_hrpears, edit_hrpears, delete_hrpears

notifs = Blueprint('notifs', __name__, template_folder='templates')

#===============================================================================================================================>
#                //\\     ||*****,   ||\\        //|| || ||\\    ||
#               //  \\    ||      || || \\      // || || || \\   ||
#              //****\\   ||      || ||  \\    //  || || ||  \\  ||
#             //******\\  ||      || ||   \\  //   || || ||   \\ ||
#            //        \\ ||____ ,*  ||    \\//    || || ||    \\||
#================ Admin ========================================================================================================>

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
    total_user = len(user_data)
    role_data = Roles.get_all()
    total_role = len(role_data)
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
                           total_login_data=total_login_data)

@notifs.route('/login', methods=['GET', 'POST'])
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
                    flash('Invalid username or password', 'danger')
            else:
                flash('Invalid username or password', 'danger')
        return render_template('login.html')

    except requests.exceptions.RequestException:
        flash('There was an issue with the login request.', 'danger')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    return render_template('login.html')

@notifs.route('/logout')
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
@notifs.route('/register_user', methods=['POST'])#add user
@login_required
def register_user():
    new_user = add_user()
    try:
        role = Roles.get_by_id(new_user.role_id)
        if new_user:
            activity = f"ADDED {new_user.full_name} as {role.role_name} to Users."
            flash('User Credentials added successfully!', 'success')
        else:
            activity = f"FAILED TO ADD User Credentials. Missing or invalid data."
            flash('Failed to add User credentials.', 'danger')
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback() 
        activity = f"FAILED TO ADD User Credentials due to error: {str(e)}."
        add_user_logs(activity)
        db.session.commit()
        flash(f"Error: {str(e)}", 'danger')
    return redirect(url_for('notifs.admin'))
    
@notifs.route('/edit_user/<int:user_id>', methods=['POST'])#edit user
@login_required
def edit_user(user_id):
    try:
        updated_user_data = edit_user(user_id, request.form)
        return jsonify({'message': 'User updated successfully', 'user': updated_user_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400








@notifs.route('/delete_user/<int:user_id>', methods=['DELETE'])#delete user
@login_required
def delete_user(user_id):
    try:
        result = delete_user(user_id)
        return result
    except Exception as e:
        return jsonify({'error': str(e)}), 500






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
            flash('Failed to add iTexMo credentials.', 'danger')
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
        flash(f"Error: {str(e)}", 'danger')
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
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()

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
            flash('Failed to add Login API credentials.', 'danger')
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
        flash(f"Error: {str(e)}", 'danger')
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
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()

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
            activity = f"ADDED {new_ecredss.ecreds_email} to Email API Credentials."
            flash('Email API credentials added successfully!', 'success')
        else:
            activity = f"FAILED TO ADD Email API Credentials. Missing or invalid data."
            flash('Failed to add Email API credentials.', 'danger')
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
        flash(f"Error: {str(e)}", 'danger')
    return redirect(url_for('notifs.admin'))

@notifs.route('/edit_email_route/<int:ecreds_id>', methods=['POST'])#edit email API credentials
@login_required
def edit_email_route(ecreds_id):
    ecreds_data = Ecredss.get_by_id(ecreds_id)
    cur_email = ecreds_data.ecreds_email
    cur_sender = ecreds_data.ecreds_sender
    cur_password = ecreds_data.ecreds_password
    cur_template = ecreds_data.ecreds_templates
    
    new_email = request.form.get('ecreds_email')
    new_sender = request.form.get('ecreds_sender')
    new_password = request.form.get('ecreds_password')
    new_template = request.form.get('ecreds_templates')
    try:
        if edit_ecreds(ecreds_id):
            activity = f"EDIT Email API Credentials from: [{cur_email},{cur_sender},{cur_password},{cur_template}]to [{new_email},{new_sender},{new_password},{new_template}]."
            flash('Email API Credential updated successfully', 'success')
        else:
            activity = f"FAILED TO EDIT Email Credentials. Missing or invalid data."
            flash('Email API record not found or update failed', 'error')
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()

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
        activity = f"DELETE {ecreds_data.ecreds_email} from Email API Credentials."
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
            flash('Failed to add Hrpears API credentials.', 'danger')
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
        flash(f"Error: {str(e)}", 'danger')
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
            add_user_logs(activity)
            db.session.commit()
            return redirect(url_for('notifs.admin'))
        add_user_logs(activity)
        db.session.commit()

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
        activity = f"DELETE {hrpears_data.hrpears_host} from HRpears API Credentials."
        flash('HRpears API record deleted successfully', 'success')
    except Exception as e:
        activity = f"FAILED TO DELETE HRpears API Credentials due to error: {str(e)}."
        flash('An error occurred while deleting the record.', 'error')
    add_user_logs(activity)
    db.session.commit()
    return redirect(request.referrer)





#===============================================================================================================================>
#
#
#
#
#
#================ Home =========================================================================================================>

@notifs.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html")

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
#================ Reports ======================================================================================================>

@notifs.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    return render_template('reports.html')

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
