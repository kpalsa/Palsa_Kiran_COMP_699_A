from extensions import db
from models.account import Account
from datetime import datetime, timedelta
from models.food_record import FoodRecord
from models.risk_result import RiskResult
from models.risk_window import RiskWindow
from services.detector import Detector


class User(Account):
    __tablename__ = "users"

    id = db.Column(db.Integer, db.ForeignKey('accounts.id'), primary_key=True)
    alert_enabled = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.String(50), default="UTC")

    # =========================
    # PROFILE MANAGEMENT
    # =========================

    def update_profile(self, timezone=None, alert_enabled=None):
        if timezone:
            self.timezone = timezone
        if alert_enabled is not None:
            self.alert_enabled = alert_enabled

        db.session.commit()
        return True

    # =========================
    # FOOD RECORD MANAGEMENT
    # =========================

    def record_food(self, item, time, snack_type, planned, mood_note=None, activity=None):
        record = FoodRecord(
            item=item,
            time=time,
            snack_type=snack_type,
            planned=planned,
            user_id=self.id
        )

        db.session.add(record)
        db.session.commit()

        # Optional mood note
        if mood_note or activity:
            from models.mood_note import MoodNote
            note = MoodNote(
                text=mood_note,
                activity=activity,
                record_id=record.id
            )
            db.session.add(note)
            db.session.commit()

        return record

    def edit_food(self, record_id, new_data):
        record = FoodRecord.query.get(record_id)

        if not record or record.user_id != self.id:
            return False

        # Allow edit only same day
        if record.created_at.date() != datetime.utcnow().date():
            return False

        record.item = new_data.get("item", record.item)
        record.snack_type = new_data.get("snack_type", record.snack_type)
        record.planned = new_data.get("planned", record.planned)

        db.session.commit()
        return True

    def delete_food(self, record_id):
        record = FoodRecord.query.get(record_id)

        if not record or record.user_id != self.id:
            return False

        if record.created_at.date() != datetime.utcnow().date():
            return False

        db.session.delete(record)
        db.session.commit()
        return True

    # =========================
    # HISTORY & SUMMARY
    # =========================

    def view_history(self, days=1):
        start_date = datetime.utcnow() - timedelta(days=days)

        records = FoodRecord.query.filter(
            FoodRecord.user_id == self.id,
            FoodRecord.created_at >= start_date
        ).all()

        return records

    def filter_history(self, start_date, end_date):
        records = FoodRecord.query.filter(
            FoodRecord.user_id == self.id,
            FoodRecord.created_at >= start_date,
            FoodRecord.created_at <= end_date
        ).all()

        return records

    def clear_demo_records(self):
        FoodRecord.query.filter_by(user_id=self.id).delete()
        db.session.commit()
        return True

    # =========================
    # ML RISK ANALYSIS
    # =========================

    def view_risk_prediction(self):
        records = FoodRecord.query.filter_by(user_id=self.id).all()

        if not records:
            return None

        detector = Detector()
        score, label, explanation, risk_window = detector.analyze(records)

        result = RiskResult(
            score=score,
            label=label,
            explanation=explanation,
            user_id=self.id
        )

        db.session.add(result)
        db.session.commit()

        return result

    def get_frequent_snack_windows(self):
        records = FoodRecord.query.filter_by(user_id=self.id).all()

        detector = Detector()
        return detector.identify_risky_windows(records)

    # =========================
    # ALERT SETTINGS
    # =========================

    def toggle_alerts(self, status: bool):
        self.alert_enabled = status
        db.session.commit()
        return True

    # =========================
    # EXPORT SUMMARY (SIMPLIFIED)
    # =========================

    def export_summary(self):
        records = FoodRecord.query.filter_by(user_id=self.id).all()

        summary = []
        for r in records:
            summary.append({
                "item": r.item,
                "time": r.time,
                "type": r.snack_type,
                "planned": r.planned
            })

        return summary

    # =========================
    # UTILITY
    # =========================

    def __repr__(self):
        return f"<User {self.email}>"