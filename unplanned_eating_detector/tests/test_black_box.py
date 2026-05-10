import unittest
from app import create_app
from extensions import db


class TestBlackBox(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_register(self):
        response = self.client.post("/register", data={
            "email": "user1@test.com",
            "password": "123"
        })

        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.client.post("/login", data={
            "email": "user1@test.com",
            "password": "123"
        })

        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_access(self):
        response = self.client.get("/dashboard")
        self.assertIn(response.status_code, [200, 302])

    def test_risk_without_data(self):
        response = self.client.get("/risk")
        self.assertIn(response.status_code, [200, 302])


if __name__ == "__main__":
    unittest.main()