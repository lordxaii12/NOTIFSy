from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import login_required, logout_user
from flask_migrate import Migrate
from config import Config
from flask_login import login_user, current_user
from utils import get_manila_time
import requests

#Models
from models.user import User_v1
from models.role import Roles
from models.user_logs import User_logs
from models.user_division import Divisions
from models.external_contacts import External
from models.login_api import LogApi
from models.themes import Theme
from models.itexmo_api import Itexmo

#Controllers
from controllers.role import add_role, edit_role, delete_role
from controllers.user import add_user, edit_user, delete_user, change_theme
from controllers.user_logs import add_user_logs, delete_user_logs
from controllers.user_division import add_division, edit_division, delete_division
from controllers.external_contacts import add_external, edit_external, delete_external
from controllers.login_api import add_login_api, edit_login_api, delete_login_api
from controllers.themes import add_theme, edit_theme, delete_theme
from controllers.itexmo_api import add_itexmo, edit_itexmo, delete_itexmo

notifs = Blueprint('notifs', __name__, template_folder='templates')


#================ Admin ========================================================================================================>

@notifs.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user_data = User_v1.get_all()
    role_data = Roles.get_all()
    return render_template('admin.html',role_data=role_data, user_data=user_data)

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
    new_itexmo = add_itexmo()
    if new_itexmo is None:
        return redirect(url_for('notifs.admin'))
    flash("Error adding iTexMo", "error")
    return redirect(url_for('notifs.admin')) 



@notifs.route('/edit_itexmo_route/<int:itexmo_id>', methods=['POST'])
@login_required
def edit_itexmo_route(itexmo_id):
    try:
        updated_itexmo = edit_itexmo(itexmo_id, request.form)
        if not updated_itexmo:
            flash('iTexMo record not found or update failed', 'error')
            return redirect(url_for('notifs.admin'))
        flash('iTexMo record updated successfully', 'success')
        return redirect(url_for('notifs.admin'))
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('notifs.admin'))


   
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
