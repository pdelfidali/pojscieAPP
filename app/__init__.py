from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Niech ktoś coś tu wpisze'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    @app.route('/index')
    @app.route('/')
    def index():
        return  render_template('index.html')


    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.events import events as events_blueprint
    app.register_blueprint(events_blueprint)

    return app
