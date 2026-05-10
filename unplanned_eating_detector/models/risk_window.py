from extensions import db
from datetime import datetime


class RiskWindow(db.Model):
    __tablename__ = "risk_windows"

    id = db.Column(db.Integer, primary_key=True)

    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)

    risk_level = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional link to user (can be global or user-specific)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # =========================
    # CORE METHODS
    # =========================

    def save(self):
        """Save risk window"""
        db.session.add(self)
        db.session.commit()
        return True

    def update_window(self, start_time=None, end_time=None, risk_level=None):
        """Update risk window values"""
        if start_time:
            self.start_time = start_time
        if end_time:
            self.end_time = end_time
        if risk_level:
            self.risk_level = risk_level

        db.session.commit()
        return True

    def delete_window(self):
        """Delete risk window"""
        db.session.delete(self)
        db.session.commit()
        return True

    # =========================
    # HELPER METHODS
    # =========================

    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "risk_level": self.risk_level,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

    @staticmethod
    def create_window(start, end, risk_level="High Risk", user_id=None):
        """
        Create new risk window
        """
        window = RiskWindow(
            start_time=start,
            end_time=end,
            risk_level=risk_level,
            user_id=user_id
        )

        db.session.add(window)
        db.session.commit()

        return window

    @staticmethod
    def get_user_windows(user_id):
        """
        Get risk windows for a specific user
        """
        return RiskWindow.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_windows():
        """
        Get all windows (admin)
        """
        return RiskWindow.query.all()

    # =========================
    # LOGIC SUPPORT METHODS
    # =========================

    def matches_time(self, current_time_str):
        """
        Check if a given time falls within this window
        (simple string-based logic for demo)
        """
        try:
            current = int(current_time_str.split(":")[0])
            start = int(self.start_time.split(":")[0])
            end = int(self.end_time.split(":")[0])

            return start <= current <= end
        except:
            return False

    # =========================
    # REPRESENTATION
    # =========================

    def __repr__(self):
        return f"<RiskWindow {self.start_time} - {self.end_time} ({self.risk_level})>"