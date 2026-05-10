from extensions import db
from datetime import datetime


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.String(255), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    delivered = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key → User (nullable for admin broadcast)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # =========================
    # CORE METHODS
    # =========================

    def schedule(self, message, scheduled_time, user_id=None):
        """
        Create and schedule an alert
        """
        self.message = message
        self.scheduled_time = scheduled_time
        self.user_id = user_id
        self.delivered = False

        db.session.add(self)
        db.session.commit()
        return True

    def mark_as_delivered(self):
        """
        Mark alert as delivered
        """
        self.delivered = True
        db.session.commit()
        return True

    def send_now(self):
        """
        Immediately send alert (simulation)
        """
        self.delivered = True
        db.session.commit()
        return self.message

    # =========================
    # ALERT LOGIC
    # =========================

    def is_due(self):
        """
        Check if alert time has arrived
        """
        return datetime.utcnow() >= self.scheduled_time and not self.delivered

    def generate_default_message(self, risk_level, time_window=None):
        """
        Generate smart alert message
        """
        if risk_level == "High Risk":
            msg = "You usually snack during this time. Try to avoid unplanned eating."
        elif risk_level == "Medium Risk":
            msg = "Be mindful of your eating habits around this time."
        else:
            msg = "Keep maintaining your healthy eating pattern."

        if time_window:
            msg += f" Risk window: {time_window}"

        self.message = msg
        return self.message

    # =========================
    # QUERY HELPERS
    # =========================

    @staticmethod
    def get_pending_alerts(user_id):
        """
        Get all pending alerts for user
        """
        return Alert.query.filter_by(
            user_id=user_id,
            delivered=False
        ).all()

    @staticmethod
    def get_all_alerts(user_id):
        """
        Get all alerts for user
        """
        return Alert.query.filter_by(user_id=user_id).all()

    # =========================
    # HELPER METHODS
    # =========================

    def to_dict(self):
        return {
            "message": self.message,
            "scheduled_time": self.scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "delivered": self.delivered
        }

    # =========================
    # REPRESENTATION
    # =========================

    def __repr__(self):
        return f"<Alert {self.message}>"