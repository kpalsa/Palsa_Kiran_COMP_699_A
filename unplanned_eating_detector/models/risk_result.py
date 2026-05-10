from extensions import db
from datetime import datetime


class RiskResult(db.Model):
    __tablename__ = "risk_results"

    id = db.Column(db.Integer, primary_key=True)

    score = db.Column(db.Float, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    explanation = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key → User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # =========================
    # CORE METHODS
    # =========================

    def save(self):
        """Save risk result"""
        db.session.add(self)
        db.session.commit()
        return True

    def generate_label(self):
        """
        Convert score → label
        """
        if self.score >= 0.7:
            self.label = "High Risk"
        elif self.score >= 0.4:
            self.label = "Medium Risk"
        else:
            self.label = "Low Risk"

        return self.label

    def generate_explanation(self, factors: dict):
        """
        Create explanation based on factors
        """
        explanation_parts = []

        if factors.get("late_night"):
            explanation_parts.append("Frequent late-night snacking detected")

        if factors.get("high_frequency"):
            explanation_parts.append("High snack frequency observed")

        if factors.get("unplanned_ratio"):
            explanation_parts.append("Large number of unplanned snacks")

        if factors.get("stress_eating"):
            explanation_parts.append("Snacking linked with stress or mood")

        if not explanation_parts:
            explanation_parts.append("No major unhealthy pattern detected")

        self.explanation = ". ".join(explanation_parts)
        return self.explanation

    def is_high_risk(self):
        return self.score >= 0.7

    # =========================
    # HELPER METHODS
    # =========================

    def to_dict(self):
        return {
            "score": round(self.score, 2),
            "label": self.label,
            "explanation": self.explanation,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }

    # =========================
    # REPRESENTATION
    # =========================

    def __repr__(self):
        return f"<RiskResult {self.label} ({self.score})>"