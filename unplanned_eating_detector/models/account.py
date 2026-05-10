from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # AUTH METHODS
    # =========================

    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def login(self, password):
        """Login validation"""
        if self.status != "active":
            return False, "Account is not active"

        if self.check_password(password):
            return True, "Login successful"
        else:
            return False, "Invalid credentials"

    def logout(self):
        """Logout logic (handled by session)"""
        return True

    def reset_password(self, new_password):
        """Reset password"""
        self.set_password(new_password)
        db.session.commit()
        return True

    # =========================
    # UTILITY METHODS
    # =========================

    def deactivate(self):
        self.status = "inactive"
        db.session.commit()

    def activate(self):
        self.status = "active"
        db.session.commit()

    def to_dict(self):
        """Convert object to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "status": self.status,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Account {self.email}>"