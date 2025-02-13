from models.user_logs import User_logs
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

def add_user_logs(activity):
    user = current_user.full_name
    created_on = get_manila_time()
    
    new_logss = User_logs(
        user=user,
        activity=activity,
        created_on=created_on
    )
    db.session.add(new_logss)
    db.session.commit()

    flash("User added successfully", "success")
    return new_logss
    

def delete_user_logs(log_id):
    user_logs = User_logs.get_by_id(log_id)
    if not user_logs:
        return jsonify({'error': 'user_logs not found'}), 404
    try:
        db.session.delete(user_logs)
        db.session.commit()
        return jsonify({'message': 'user_logs deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500