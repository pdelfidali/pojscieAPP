from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    app.config['SECRET_KEY'] = 'Niech ktoś coś tu wpisze'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
