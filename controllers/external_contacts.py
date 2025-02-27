#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.external_contacts import External
from extensions import db
from flask import request, jsonify, flash
from flask_login import current_user
from utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
def add_external():
    external_name = request.form.get('external_name')
    external_mobile = request.form.get('external_mobile')
    external_email = request.form.get('external_email')
    external_description = request.form.get('external_description')
    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_externals = External(
        external_name=external_name,
        external_mobile=external_mobile,
        external_email=external_email,
        external_description=external_description,
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_externals)
    db.session.commit()

    flash("Contact added successfully", "success")
    return new_externals 

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================> 
def edit_external(external_id):
    external = External.get_by_id(external_id)
    
    external_name = request.form.get('external_name',external.external_name)
    external_description = request.form.get('external_description',external.external_description)
    external_mobile = request.form.get('external_mobile',external.external_mobile)
    external_email = request.form.get('external_email',external.external_email)
    
    updated_by = current_user.full_name
    updated_on = get_manila_time()
   
    external.external_name = external_name
    external.external_description = external_description
    external.external_mobile = external_mobile
    external.external_email = external_email
    external.updated_by = updated_by
    external.updated_on = updated_on
    
    try:
        external.save()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#===============================================================================================================================>
#
#================ EDIT =========================================================================================================>
def delete_external(external_id):
    external = External.get_by_id(external_id)
    try:
        db.session.delete(external)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

#===============================================================================================================================>