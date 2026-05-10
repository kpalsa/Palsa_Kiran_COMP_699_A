from extensions import db
from models.account import Account
from datetime import datetime, timedelta
from models.food_record import FoodRecord
from models.alert import Alert
from models.risk_window import RiskWindow


class SystemAdmin(Account):
    __tablename__ = "admins"

    id = db.Column(db.Integer, db.ForeignKey('accounts.id'), primary_key=True)
    admin_role = db.Column(db.String(50), default="standard")

    # =========================
    # DASHBOARD DATA
    # =========================

    def view_dashboard(self, days=7):
        """
        Returns summary dashboard data
        """
        start_date = datetime.utcnow() - timedelta(days=days)

        total_records = FoodRecord.query.filter(
            FoodRecord.created_at >= start_date
        ).count()

        unplanned_count = FoodRecord.query.filter(
            FoodRecord.created_at >= start_date,
            FoodRecord.planned == False
        ).count()

        alert_count = Alert.query.filter(
            Alert.created_at >= start_date
        ).count()

        return {
            "total_records": total_records,
            "unplanned_snacks": unplanned_count,
            "alerts_triggered": alert_count
        }

    # =========================
    # RISK WINDOW ANALYSIS
    # =========================

    def get_common_risky_windows(self):
        """
        Returns common risky time windows across users
        """
        windows = RiskWindow.query.all()

        result = []
        for w in windows:
            result.append({
                "start": w.start_time,
                "end": w.end_time,
                "risk_level": w.risk_level
            })

        return result

    # =========================
    # ALERT FREQUENCY
    # =========================

    def get_alert_frequency(self, days=7):
        """
        Count alerts per week
        """
        start_date = datetime.utcnow() - timedelta(days=days)

        alerts = Alert.query.filter(
            Alert.created_at >= start_date
        ).all()

        return len(alerts)

    # =========================
    # FILTER DASHBOARD
    # =========================

    def filter_dashboard(self, start_date, end_date):
        records = FoodRecord.query.filter(
            FoodRecord.created_at >= start_date,
            FoodRecord.created_at <= end_date
        ).all()

        return records

    # =========================
    # GUIDANCE MESSAGES
    # =========================

    def publish_guidance(self, message):
        """
        Store admin message (simple implementation)
        """
        alert = Alert(
            message=message,
            scheduled_time=datetime.utcnow(),
            delivered=True,
            user_id=None  # broadcast
        )

        db.session.add(alert)
        db.session.commit()

        return True

    def add_guidance_note(self, message):
        """
        Alias for publishing guidance
        """
        return self.publish_guidance(message)

    # =========================
    # UTILITY
    # =========================

    def __repr__(self):
        return f"<Admin {self.email}>"