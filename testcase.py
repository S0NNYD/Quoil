import unittest
from website import create_app, db
from website.models import Userlogin

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # create a test user
        test_user = Userlogin(username='testuser', password='testpass')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_success(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpass'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        #self.assertIn(b'Logged in Successfully!', response.data)

    def test_login_invalid_password(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='wrongpass'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect password, try again.', response.data)

    def test_login_nonexistent_user(self):
        response = self.client.post('/login', data=dict(
            username='nonexistent',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account does not exist.', response.data)

if __name__ == '__main__':
    unittest.main()