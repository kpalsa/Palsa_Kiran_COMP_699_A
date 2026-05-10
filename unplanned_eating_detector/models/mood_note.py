from extensions import db
from datetime import datetime


class MoodNote(db.Model):
    __tablename__ = "mood_notes"

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(255), nullable=True)
    activity = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key → FoodRecord
    record_id = db.Column(db.Integer, db.ForeignKey('food_records.id'), nullable=False)

    # =========================
    # CORE METHODS
    # =========================

    def attach_to_record(self, record_id):
        """
        Attach note to a food record
        """
        self.record_id = record_id
        db.session.add(self)
        db.session.commit()
        return True

    def update_note(self, text=None, activity=None):
        """
        Update mood/activity
        """
        if text is not None:
            self.text = text
        if activity is not None:
            self.activity = activity

        db.session.commit()
        return True

    def delete_note(self):
        """
        Delete mood note
        """
        db.session.delete(self)
        db.session.commit()
        return True

    # =========================
    # HELPER METHODS
    # =========================

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "activity": self.activity,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

    def is_empty(self):
        """
        Check if note has no meaningful data
        """
        return not self.text and not self.activity

    # =========================
    # REPRESENTATION
    # =========================

    def __repr__(self):
        return f"<MoodNote {self.id}>"