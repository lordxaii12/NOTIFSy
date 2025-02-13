from flask import Flask, render_template
from flask_login import LoginManager, current_user
from config import Config
from extensions import db
from flask_migrate import Migrate
from models.user import User_v1
from routes import notifs
from sqlalchemy.exc import OperationalError
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "notifs.login" 

    @login_manager.user_loader
    def load_user(user_id):
        return User_v1.get_by_id(int(user_id))

    db.init_app(app)

    @app.errorhandler(OperationalError)
    def handle_operational_error(error):
        app.logger.error(f"OperationalError: {error}")
        return render_template("error.html", message="Database connection failed. Please check the server.")

    try:
        with app.app_context():
            db.engine.connect() 
    except OperationalError as e:
        app.logger.error(f"OperationalError: {e}")
        app.logger.error(f"Database connection failed: {e}")
        raise OperationalError("Database connection failed. Please check the server.") from e

    app.register_blueprint(notifs)
    
    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
