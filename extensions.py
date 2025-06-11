#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from celery import Celery
#===============================================================================================================================>
cache = Cache()
db = SQLAlchemy()
limiter = Limiter(get_remote_address, default_limits=["5 per minute"])
celery = Celery(__name__)
#===============================================================================================================================>

