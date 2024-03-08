from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()  # could do in import I think
DB_NAME = "database.db"  # filename gnerated in 'instance' folder

"""Main app created"""


def create_app():
    app = Flask(__name__)  # create Flask app
    app.config["SECRET_KEY"] = "asdf"  # this is a dummy value, should be more
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"  # URI=path I think
    db.init_app(app)  # starts app, server, whatever

    from .views import views  # import calls for HTML creation/sending
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")  # ties views into html templates
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note  # imports db models (tables)

    create_database(app)  # create DB if it doesn't already exist

    """I don't follow all this, but the gist is as expected."""
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


"""Create database.db if it doesn't exist currently"""


def create_database(app):
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")
