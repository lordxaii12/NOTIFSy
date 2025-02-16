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

#Controllers
from controllers.user_role import add_role, edit_role, delete_role
from controllers.user import add_user, edit_user, delete_user, change_theme
from controllers.user_logs import add_user_logs, delete_user_logs
from controllers.user_division import add_division, edit_division, delete_division
from controllers.external_credentials import add_external, edit_external, delete_external
from controllers.login_credentials import add_login_api, edit_login_api, delete_login_api
from controllers.user_themes import add_theme, edit_theme, delete_theme
from controllers.itexmo_credentials import add_itexmo, edit_itexmo, delete_itexmo

notifs = Blueprint('notifs', __name__, template_folder='templates')


#================ Admin ========================================================================================================>

@notifs.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    itexmo_data = Itexmo.get_all()
    total_itexmo = len(itexmo_data)
    user_data = User_v1.get_all()
    role_data = Roles.get_all()
    return render_template('admin.html',
                           role_data=role_data,
                           user_data=user_data,
                           itexmo_data=itexmo_data,
                           total_itexmo=total_itexmo)

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
    logout_user()  # Log out the current user
    flash('You have been logged out.', 'info')
    return redirect(url_for('notifs.login'))  # Redirect to login page

@notifs.route('/register_user', methods=['POST'])
@login_required
def register_user():
    new_user = add_user()
    if new_user is None:
        return redirect(url_for('notifs.admin')) 
    return redirect(url_for('notifs.admin')) 

@notifs.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    try:
        updated_user_data = edit_user(user_id, request.form)
        return jsonify({'message': 'User updated successfully', 'user': updated_user_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@notifs.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    try:
        result = delete_user(user_id)
        return result
    except Exception as e:
        return jsonify({'error': str(e)}), 500











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
        activity = f"DELETE {creds_data.itexmo_name} to Itexmo Credentials."
        flash('iTexMo record deleted successfully', 'success')
    except Exception as e:
        activity = f"FAILED TO DELETE iTexMo Credentials due to error: {str(e)}."
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
