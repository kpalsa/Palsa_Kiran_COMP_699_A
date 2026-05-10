from services.ml_model import MLModel
from models.risk_window import RiskWindow
from datetime import datetime


class Detector:

    def __init__(self):
        self.model = MLModel()

    def analyze(self, records):
        """
        Main analysis function
        """

        if not records:
            return 0.0, "Low Risk", "No data available", None

        # =========================
        # FEATURE EXTRACTION
        # =========================

        total = len(records)
        unplanned = sum(1 for r in records if not r.planned)

        late_night = sum(
            1 for r in records if r.time.hour >= 21 or r.time.hour <= 5
        )

        # Binary features
        f1 = 1 if late_night > 2 else 0
        f2 = 1 if total > 5 else 0
        f3 = 1 if (unplanned / total) > 0.5 else 0

        features = [f1, f2, f3]

        # =========================
        # ML PREDICTION
        # =========================

        score = self.model.predict_risk(features)

        # =========================
        # LABEL
        # =========================

        if score >= 0.7:
            label = "High Risk"
        elif score >= 0.4:
            label = "Medium Risk"
        else:
            label = "Low Risk"

        # =========================
        # EXPLANATION
        # =========================

        factors = {
            "late_night": f1,
            "high_frequency": f2,
            "unplanned_ratio": f3,
            "stress_eating": False
        }

        explanation = self._generate_explanation(factors)

        # =========================
        # RISK WINDOW
        # =========================

        risk_window = self.identify_risky_windows(records)

        return score, label, explanation, risk_window

    # =========================
    # EXPLANATION LOGIC
    # =========================

    def _generate_explanation(self, factors):
        messages = []

        if factors["late_night"]:
            messages.append("Late-night snacking detected")

        if factors["high_frequency"]:
            messages.append("Frequent snacking behavior observed")

        if factors["unplanned_ratio"]:
            messages.append("High number of unplanned snacks")

        if not messages:
            messages.append("Eating behavior appears balanced")

        return ". ".join(messages)

    # =========================
    # RISK WINDOW DETECTION
    # =========================

    def identify_risky_windows(self, records):
        """
        Detect common risky hour
        """
        if not records:
            return None

        hours = [r.time.hour for r in records]

        # Find most common hour
        common_hour = max(set(hours), key=hours.count)

        start = f"{common_hour}:00"
        end = f"{(common_hour + 1) % 24}:00"

        window = RiskWindow.create_window(
            start=start,
            end=end,
            risk_level="High Risk"
        )

        return window