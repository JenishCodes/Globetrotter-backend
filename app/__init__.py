from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("app.config.Config")

    # Initialize extensions
    from app import models as _

    db.init_app(app)

    # Enable CORS
    CORS(app)

    return app


def load_app_modules(app):
    # Register routes
    from app.routes import main, auth, question, user, session

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(question)
    app.register_blueprint(user)
    app.register_blueprint(session)


def greceful_shutdown(_, __):
    print("Shutting down app...")
    exit(0)
