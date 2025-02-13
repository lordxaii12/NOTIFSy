import os
import pymysql

with open('config.txt', 'r') as file:
    config = {}

    for line in file:
        key, value = line.strip().split(' = ')
        config[key] = value

# Now you can access the values using the keys
secret_key = config['secret_key']
database_uri_head1 = config['database_uri_head1']
database_uri_head2 = config['database_uri_head2']
db_user = config['db_user']
db_password = config['db_password']
db_host = config['db_host']
db_port = config['db_port']
dbname = config['dbname']
db_track_mod = config['db_track_mod']
password = str(db_password)


uri = f"{database_uri_head1}+{database_uri_head2}://{db_user}:@{db_host}:{db_port}/{dbname}"

class Config:
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = uri.strip()
    SQLALCHEMY_TRACK_MODIFICATIONS = db_track_mod
