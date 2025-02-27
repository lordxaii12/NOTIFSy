#--CODE BY: RYRUBIO--#
#===============================================================================================================================>
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
#===============================================================================================================================>
cache = Cache()
db = SQLAlchemy()
limiter = Limiter(get_remote_address, default_limits=["5 per minute"])
#===============================================================================================================================>

