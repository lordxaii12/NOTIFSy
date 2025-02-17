from models.hrpears_credentials import Hrpears
from extensions import db
from flask import request
from flask_login import current_user
from utils import get_manila_time

def add_hrpears():
    hrpears_host = request.form.get('hrpears_host')
    hrpears_root = request.form.get('hrpears_root')
    hrpears_user = request.form.get('hrpears_user')
    hrpears_password = request.form.get('hrpears_password')
    hrpears_dbname = request.form.get('hrpears_dbname')
    hrpears_table = request.form.get('hrpears_table')

    
    created_by = current_user.full_name
    created_on = get_manila_time()

    new_hrpears = Hrpears(
        hrpears_host=hrpears_host,
        hrpears_root=hrpears_root,
        hrpears_user=hrpears_user,
        hrpears_password=hrpears_password,
        hrpears_dbname=hrpears_dbname,
        hrpears_table=hrpears_table,
        
        created_by=created_by,
        created_on=created_on
    )
    db.session.add(new_hrpears)
    db.session.commit()

    return new_hrpears 
    
def edit_hrpears(hrpears_id):
    hrpears = Hrpears.get_by_id(hrpears_id)
    hrpears.hrpears_host = request.form.get('hrpears_host', hrpears.hrpears_host)
    hrpears.hrpears_root = request.form.get('hrpears_root', hrpears.hrpears_root)
    hrpears.hrpears_user = request.form.get('hrpears_user', hrpears.hrpears_user)
    hrpears.hrpears_password = request.form.get('hrpears_password', hrpears.hrpears_password)
    hrpears.hrpears_dbname = request.form.get('hrpears_dbname', hrpears.hrpears_dbname)
    hrpears.hrpears_table = request.form.get('hrpears_table', hrpears.hrpears_table)
    
    hrpears.updated_by = current_user.full_name
    hrpears.updated_on = get_manila_time()

    try:
        hrpears.save()
        return hrpears  
    except Exception as e:
        db.session.rollback()
        return None  
    
def delete_hrpears(hrpears_id):
    hrpears = Hrpears.get_by_id(hrpears_id)
    try:
        db.session.delete(hrpears)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
