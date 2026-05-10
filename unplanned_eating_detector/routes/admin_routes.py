from flask import Blueprint, render_template, request, session, redirect
from models.admin import SystemAdmin
from extensions import db   # ✅ IMPORTANT FIX

admin_bp = Blueprint('admin', __name__)


# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect("/login")

    admin = SystemAdmin.query.get(session["admin_id"])

    if not admin:
        return redirect("/login")

    data = admin.view_dashboard()
    windows = admin.get_common_risky_windows()
    alerts = admin.get_alert_frequency()

    return render_template(
        "admin_dashboard.html",
        data=data,
        windows=windows,
        alerts=alerts
    )


# =========================
# PUBLISH MESSAGE
# =========================
@admin_bp.route("/admin/publish", methods=["POST"])
def publish():
    if "admin_id" not in session:
        return redirect("/login")

    admin = SystemAdmin.query.get(session["admin_id"])

    if not admin:
        return redirect("/login")

    message = request.form.get("message")

    if message:
        admin.publish_guidance(message)

    return redirect("/admin/dashboard")