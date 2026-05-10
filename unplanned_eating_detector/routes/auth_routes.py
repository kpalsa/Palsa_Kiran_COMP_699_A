from flask import Blueprint, render_template, request, redirect, session
from extensions import db
from models.user import User
from models.admin import SystemAdmin

auth_bp = Blueprint('auth', __name__)


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists"

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # =========================
        # CHECK USER
        # =========================
        user = User.query.filter_by(email=email).first()
        if user:
            valid, _ = user.login(password)
            if valid:
                session.clear()
                session["user_id"] = user.id
                session["role"] = "user"
                return redirect("/dashboard")

        # =========================
        # CHECK ADMIN
        # =========================
        admin = SystemAdmin.query.filter_by(email=email).first()
        if admin:
            valid, _ = admin.login(password)
            if valid:
                session.clear()
                session["admin_id"] = admin.id
                session["role"] = "admin"
                return redirect("/admin/dashboard")

        return "Invalid email or password"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")