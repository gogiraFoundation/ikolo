import unittest
from user_management import app

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_register_user(self):
        response = self.app.post('/register', json={"username": "test_user", "password": "test_pass"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))

    def test_login_user(self):
        self.app.post('/register', json={"username": "test_user", "password": "test_pass"})
        response = self.app.post('/login', json={"username": "test_user", "password": "test_pass"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

if __name__ == '__main__':
    unittest.main()
