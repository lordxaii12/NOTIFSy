from extensions import cache
from models.user import User_v1
from models.user_role import Roles
from models.user_logs import User_logs
from models.user_division import Divisions
from models.external_contacts import External
from models.login_credentials import LogApi
from models.user_themes import Theme
from models.itexmo_credentials import Itexmo
from models.email_credentials import Ecredss
from models.hrpears_credentials import Hrpears
from models.system_settings import SysSettings
from models.msg_log import Msg_log
from models.message_temp import Msg_templates


@cache.cached(timeout=300)
def get_cached_user():
    return User_v1.get_all()

@cache.cached(timeout=300)
def get_cached_role():
    return Roles.get_all()

@cache.cached(timeout=300)
def get_cached_user_logs():
    return User_logs.get_all()

@cache.cached(timeout=300)
def get_cached_divisions():
    return Divisions.get_all()

@cache.cached(timeout=300)
def get_cached_external_contacts():
    return External.get_all()

@cache.cached(timeout=300)
def get_cached_login_credentials():
    return LogApi.get_all()

@cache.cached(timeout=300)
def get_cached_themes():
    return Theme.get_all()

@cache.cached(timeout=300)
def get_cached_itexmo_credentials():
    return Itexmo.get_all()

@cache.cached(timeout=300)
def get_cached_email_credentials():
    return Ecredss.get_all()

@cache.cached(timeout=300)
def get_cached_hrpears_credentials():
    return Hrpears.get_all()

@cache.cached(timeout=300)
def get_cached_system_settings():
    return SysSettings.get_all()

@cache.cached(timeout=300)
def get_cached_message_logs():
    return Msg_log.get_all()

@cache.cached(timeout=300)
def get_cached_message_tempaltes():
    return Msg_templates.get_all()


