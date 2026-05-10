import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "your_secret_key_here_change_this"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # App Behavior
    DEBUG = True

    # ML Threshold
    RISK_THRESHOLD = 0.7

    # Session Config
    SESSION_TYPE = "filesystem"