#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
import os
import pymysql
from cryptography.fernet import Fernet
#===============================================================================================================================>
with open('config.txt', 'r') as file:
    config = {}

    for line in file:
        key, value = line.strip().split(' = ')
        config[key] = value
secret_key = config['secret_key'].encode()
database_uri_head1 = config['database_uri_head1']
database_uri_head2 = config['database_uri_head2']
db_user = config['db_user']
db_password = config['db_password']
if db_password == 'none':
    password =''
else:
    password = db_password
db_host = config['db_host']
db_port = config['db_port']
dbname = config['dbname']
db_track_mod = config['db_track_mod']

uri = f"{database_uri_head1}+{database_uri_head2}://{db_user}:{password}@{db_host}:{db_port}/{dbname}?charset=utf8mb4"

#===============================================================================================================================>
class Config:
    SECRET_KEY = secret_key
    cipher = Fernet(SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = uri.strip()
    SQLALCHEMY_TRACK_MODIFICATIONS = db_track_mod
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 380 
    }
    
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://127.0.0.1:6379/0'
    
#===============================================================================================================================>