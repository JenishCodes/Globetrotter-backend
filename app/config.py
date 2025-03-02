import os
import datetime

from dotenv import load_dotenv


class Config:
    # Load environment variables
    load_dotenv()

    # Application configuration
    FLASK_ENV = os.getenv("FLASK_ENV")
    DEBUG = os.getenv("DEBUG")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    # JWT configuration
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    )

    # CORS configuration
    CORS_ORIGIN = os.getenv("CORS_ORIGIN")

    # URL configuration
    URL = os.getenv("URL")
    FRONTEND_URL = os.getenv("FRONTEND_URL")
