from extensions import db
from datetime import datetime


class FoodRecord(db.Model):
    __tablename__ = "food_records"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    snack_type = db.Column(db.String(50), nullable=False)
    planned = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key → User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship → MoodNote (One-to-One)
    mood_note = db.relationship(
        "MoodNote",
        backref="food_record",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # =========================
    # CORE METHODS
    # =========================

    def save(self):
        """Save new record"""
        db.session.add(self)
        db.session.commit()
        return True

    def edit_same_day(self, new_data: dict):
        """
        Edit record only if created today
        """
        if self.created_at.date() != datetime.utcnow().date():
            return False, "Edit allowed only on same day"

        self.item = new_data.get("item", self.item)
        self.snack_type = new_data.get("snack_type", self.snack_type)
        self.planned = new_data.get("planned", self.planned)

        db.session.commit()
        return True, "Record updated"

    def delete_same_day(self):
        """
        Delete record only if created today
        """
        if self.created_at.date() != datetime.utcnow().date():
            return False, "Delete allowed only on same day"

        db.session.delete(self)
        db.session.commit()
        return True, "Record deleted"

    # =========================
    # HELPER METHODS
    # =========================

    def is_unplanned(self):
        return not self.planned

    def get_time_period(self):
        """
        Convert time → period (used for ML)
        """
        hour = self.time.hour

        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

    def to_dict(self):
        """Convert record to dictionary (for UI/JSON)"""
        return {
            "id": self.id,
            "item": self.item,
            "time": self.time.strftime("%Y-%m-%d %H:%M"),
            "snack_type": self.snack_type,
            "planned": self.planned,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

    # =========================
    # REPRESENTATION
    # =========================

    def __repr__(self):
        return f"<FoodRecord {self.item} - {self.time}>"