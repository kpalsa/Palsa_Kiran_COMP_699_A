from app import create_app, db
from models.admin import SystemAdmin

def create_super_admin():
    app = create_app()

    with app.app_context():

        email = "palsatech@admin.com"
        password = "PalsaTech@123"

        existing = SystemAdmin.query.filter_by(email=email).first()

        if existing:
            print(" Super Admin already exists")
            return

        admin = SystemAdmin(email=email)
        admin.set_password(password)
        admin.admin_role = "superadmin"

        db.session.add(admin)
        db.session.commit()

        print("✅ Super Admin Created Successfully")
        print(f"📧 Email: {email}")
        print(f"🔐 Password: {password}")


if __name__ == "__main__":
    create_super_admin()