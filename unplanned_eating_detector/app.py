from flask import Flask, render_template
from config import Config
from extensions import db   # ✅ FIXED (IMPORTANT)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize DB
    db.init_app(app)

    # ==============================
    # IMPORT MODELS (IMPORTANT)
    # ==============================
    from models.account import Account
    from models.user import User
    from models.admin import SystemAdmin
    from models.food_record import FoodRecord
    from models.mood_note import MoodNote
    from models.risk_result import RiskResult
    from models.alert import Alert
    from models.risk_window import RiskWindow

    # ==============================
    # IMPORT ROUTES
    # ==============================
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # ==============================
    # HOME ROUTE
    # ==============================
    @app.route("/")
    def home():
        return render_template("login.html")

    # ==============================
    # CREATE DATABASE TABLES
    # ==============================
    with app.app_context():
        db.create_all()

    return app


# Run App
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)