from models.email_credentials import Ecredss
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

def add_ecreds():
    ecreds_email = request.form.get('ecreds_email')
    ecreds_sender = request.form.get('ecreds_sender')
    ecreds_password = request.form.get('ecreds_password')
    ecreds_templates = request.form.get('ecreds_templates')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_ecredss = Ecredss(
        ecreds_email=ecreds_email,
        ecreds_sender=ecreds_sender,
        ecreds_password=ecreds_password,
        ecreds_templates=ecreds_templates,

        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_ecredss)
    db.session.commit()

    flash("Credentials added successfully", "success")
    return new_ecredss   
    
def edit_ecreds(ecreds_id):
    ecreds = Ecredss.get_by_id(ecreds_id)
    
    ecreds_email = request.form.get('ecreds_email',ecreds.ecreds_email)
    ecreds_sender = request.form.get('ecreds_sender',ecreds.ecreds_sender)
    ecreds_password = request.form.get('ecreds_password',ecreds.ecreds_password)
    ecreds_templates = request.form.get('ecreds_templates',ecreds.ecreds_templates)
    
    updated_by = current_user.full_name
    updated_on = get_manila_time()
   
    ecreds.ecreds_email = ecreds_email
    ecreds.ecreds_sender = ecreds_sender
    ecreds.ecreds_password = ecreds_password
    ecreds.ecreds_templates = ecreds_templates
    
    ecreds.updated_by = updated_by
    ecreds.updated_on = updated_on
    
    try:
        ecreds.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_ecreds(ecreds_id):
    ecreds = Ecredss.get_by_id(ecreds_id)
    try:
        db.session.delete(ecreds)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
