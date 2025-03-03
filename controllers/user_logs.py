#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from models.user_logs import User_logs
from extensions import db
from flask_login import current_user
from utility.sys_utils import get_manila_time

#===============================================================================================================================>
#
#================ ADD ==========================================================================================================>
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
    return new_logss

#===============================================================================================================================>
#
#================ DELETE =======================================================================================================>  
def delete_user_logs(log_id):
    user_logs = User_logs.get_by_id(log_id)

    try:
        db.session.delete(user_logs)
        db.session.commit()

    except Exception as e:
        db.session.rollback()

#===============================================================================================================================>