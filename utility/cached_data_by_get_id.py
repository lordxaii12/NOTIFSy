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


@cache.memoize(timeout=300)
def get_cached_user_id(id):
    return User_v1.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_role_id(id):
    return Roles.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_user_logs_id(id):
    return User_logs.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_divisions_id(id):
    return Divisions.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_external_contacts_id(id):
    return External.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_login_credentials_id(id):
    return LogApi.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_themes_id(id):
    return Theme.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_itexmo_credentials_id(id):
    return Itexmo.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_email_credentials_id(id):
    return Ecredss.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_hrpears_credentials_id(id):
    return Hrpears.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_system_settings_id(id):
    return SysSettings.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_message_logs_id(id):
    return Msg_log.get_by_id(id)

@cache.memoize(timeout=300)
def get_cached_message_tempaltes_id(id):
    return Msg_templates.get_by_id(id)


