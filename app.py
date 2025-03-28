#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from flask import Flask, render_template, g
from flask_login import LoginManager, current_user
from config import Config
from extensions import db , limiter, cache
from flask_migrate import Migrate
from models.system_settings import SysSettings
from models.user import User_v1
from utility.sys_utils import to_block_text, decrypt_content, encrypt_content
from routes import notifs
from sqlalchemy.exc import OperationalError
import logging

#===============================================================================================================================>
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config['CACHE_TYPE'] = 'redis' 
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    cache.init_app(app)
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
        'pool_size': 10,
        'max_overflow': 20
    } 
    
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "notifs.login" 

    @login_manager.user_loader
    def load_user(user_id):
        return User_v1.get_by_id(int(user_id))

    db.init_app(app)

    # Error handler for database connection errors
    @app.errorhandler(OperationalError)
    def handle_operational_error(error):
        app.logger.error(f"OperationalError: {error}")
        return render_template("error.html", message="Database connection failed. Please check the server."), 500

    app.register_blueprint(notifs)

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    @app.before_request
    def load_sys_settings():
        try:
            g.sys_settings = SysSettings.get_by_id(1)
        except OperationalError as e:
            app.logger.error(f"Failed to load system settings: {e}")
            return render_template("error.html", message="Database connection failed. Please check the server."), 500

    @app.context_processor
    def inject_block_text():
        return dict(to_block_text=to_block_text)

    @app.context_processor
    def inject_encryptor():
        return dict(encrypt_content=encrypt_content)

    @app.context_processor
    def inject_decryptor():
        return dict(decrypt_content=decrypt_content)

    return app
#===============================================================================================================================>
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
#===============================================================================================================================>