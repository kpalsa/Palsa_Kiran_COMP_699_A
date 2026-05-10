from flask import Blueprint, render_template, request, redirect, session
from models.user import User
from models.food_record import FoodRecord
from services.detector import Detector
from services.alert_service import AlertService
from datetime import datetime

user_bp = Blueprint('user', __name__)


# =========================
# DASHBOARD
# =========================
@user_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# =========================
# ADD FOOD
# =========================
@user_bp.route("/add_food", methods=["GET", "POST"])
def add_food():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    if not user:
        return redirect("/login")

    if request.method == "POST":
        try:
            item = request.form.get("item")
            time_str = request.form.get("time")
            snack_type = request.form.get("type")
            planned = request.form.get("planned") == "yes"
            mood = request.form.get("mood")
            activity = request.form.get("activity")

            time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")

            user.record_food(item, time, snack_type, planned, mood, activity)

            return redirect("/dashboard")

        except Exception as e:
            return f"Error adding food: {str(e)}"

    return render_template("add_food.html")


# =========================
# HISTORY
# =========================
@user_bp.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    if not user:
        return redirect("/login")

    records = user.view_history(days=7)

    return render_template("history.html", records=records)


# =========================
# RISK PAGE
# =========================
@user_bp.route("/risk")
def risk():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    if not user:
        return redirect("/login")

    result = user.view_risk_prediction()

    # Trigger alert if needed
    if result:
        records = FoodRecord.query.filter_by(user_id=user.id).all()

        if records:
            detector = Detector()
            _, _, _, window = detector.analyze(records)

            alert_service = AlertService()
            alert_service.create_alert_for_user(user, result, window)

    return render_template("risk.html", result=result)


# =========================
# DELETE FOOD
# =========================
@user_bp.route("/delete/<int:id>")
def delete_food(id):
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    if not user:
        return redirect("/login")

    user.delete_food(id)

    return redirect("/history")


# =========================
# TOGGLE ALERTS
# =========================
@user_bp.route("/toggle_alert")
def toggle_alert():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    if not user:
        return redirect("/login")

    user.toggle_alerts(not user.alert_enabled)

    return redirect("/dashboard")