import unittest
from app import create_app
from models.user import User
from models.food_record import FoodRecord
from services.detector import Detector
from datetime import datetime
from extensions import db


class TestWhiteBox(unittest.TestCase):

    def setUp(self):
        # Create Flask app
        self.app = create_app()

        # Push application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create dummy user
        self.user = User(email="test@test.com")
        self.user.set_password("123")

        # Create dummy food records
        self.records = [
            FoodRecord(
                item="Chips",
                time=datetime.now(),
                snack_type="Snack",
                planned=False
            ),
            FoodRecord(
                item="Juice",
                time=datetime.now(),
                snack_type="Drink",
                planned=True
            )
        ]

    def tearDown(self):
        # Clean database session
        db.session.remove()

        # Pop app context
        self.app_context.pop()

    def test_detector_flow(self):
        detector = Detector()

        result, score, label, window = detector.analyze(self.records)

        # Validate score
        self.assertIsNotNone(score)

        # Validate label (string output from your system)
        self.assertIsInstance(label, str)

        # Validate result object
        self.assertIsNotNone(result)

        # Validate risk window
        self.assertIsNotNone(window)


if __name__ == "__main__":
    unittest.main()