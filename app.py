#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from flask import Flask, render_template, g, make_response, has_request_context,request
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
import sys
from flask_assets import Environment, Bundle
import time

#===============================================================================================================================>
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    css = Bundle(
        'css/notif.css',
        'css/table_headers.css',
        filters='cssmin',
        output='gen/packed.css'
    )

    js = Bundle(
        'js/delete.js',
        'js/edit.js',
        'js/utils.js',
        filters='jsmin',
        output='gen/packed.js'
    )
    
    assets = Environment(app)
    assets.register('css_all', css)
    assets.register('js_all', js)
    
    app.config['CACHE_DEFAULT_TIMEOUT'] = 1800
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
        if has_request_context():
            settings = cache.get('sys_settings')
            if not settings:
                app.logger.debug("Cache miss: loading sys_settings from DB.")
                try:
                    settings = SysSettings.get_by_id(1)
                    cache.set('sys_settings', settings)
                except OperationalError as e:
                    app.logger.error(f"Failed to load system settings: {e}")
                    return render_template("error.html", message="Database connection failed. Please check the server."), 500
            g.sys_settings = settings

    @app.context_processor
    def inject_block_text():
        return dict(to_block_text=to_block_text)

    @app.context_processor
    def inject_encryptor():
        return dict(encrypt_content=encrypt_content)

    @app.context_processor
    def inject_decryptor():
        return dict(decrypt_content=decrypt_content)
    
    @app.after_request
    def add_header(response):
        if request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'public, max-age=2592000, immutable'
        else:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        duration = time.time() - request.start_time
        app.logger.info(f"{request.method} {request.path} took {duration:.4f}s")
        return response
    return app
#===============================================================================================================================>
app = create_app()
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8000
    if '--host' in sys.argv:
        host = sys.argv[sys.argv.index('--host') + 1]
    if '--port' in sys.argv:
        port = int(sys.argv[sys.argv.index('--port') + 1])
    app.run(host=host, port=port, debug=True)
#===============================================================================================================================>
