import unittest
from website import create_app, db
from flask import Flask, request, url_for,redirect
from website.models import Userlogin, User
from website.authenciation import completeReg
from website.pricing import pricing
from unittest.mock import patch
from flask_login import current_user
from flask_testing import TestCase

class TestPricing(unittest.TestCase):

    def test_total_amount(self):
        # Instantiate the pricing class with different inputs
        p1 = pricing('TX', True, 500)
        p2 = pricing('CA', False, 1500)

        # Calculate the expected total amount based on the suggested price
        total1 = p1.gal_requested * p1.get_suggested_price()
        total2 = p2.gal_requested * p2.get_suggested_price()

        # Check that the calculated total amount is correct
        self.assertEqual(p1.total_amount(), total1)
        self.assertEqual(p2.total_amount(), total2)

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # create a test user
        test_user = Userlogin(username='testuser', password='testpass', firstTime = True)
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
    
    def test_logout(self):
        with self.app.test_client() as client:
            # Log in the test user
            restest = self.client.post('/login', data=dict(
                username='testuser',
                password='testpass'
            ), follow_redirects=True)

            # Check that the user is logged in
            self.assertEqual(restest.status_code, 200)

            # Log out the user
            response = client.get('/logout', follow_redirects=True)

            # Check that the user is logged out
            self.assertFalse(current_user.is_authenticated)

            # Check that the user is redirected to the login page
            self.assertEqual(response.status_code, 200)
            #self.assertEqual(response.location, url_for('authenciator.login', _external=True))

class TestReg(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration_success(self):
        # simulate user input
        with self.client:
            response = self.client.post('/register', data=dict(
                username='testuser',
                password1='testpassword',
                password2='testpassword'
            ), follow_redirects=True)

            # check if user is added to database
            user = Userlogin.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)

            # check if success message is displayed
            self.assertIn(b'Account creation successful', response.data)

            # check if redirected to login page
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data)

    def test_username_exists(self):
        # simulate user input
        existing = Userlogin(username='existinguser', password='testpassword')
        db.session.add(existing)
        db.session.commit()
        with self.client:
            response = self.client.post('/register', data=dict(
                username='existinguser',
                password1='testpassword',
                password2='testpassword'
            ), follow_redirects=True)

            # check if error message is displayed
            self.assertIn(b'Username already exists.', response.data)

            # check if not redirected
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)

    def test_username_length(self):
        # simulate user input
        with self.client:
            response = self.client.post('/register', data=dict(
                username='tiny',
                password1='testpassword',
                password2='testpassword'
            ), follow_redirects=True)

            # check if error message is displayed
            self.assertIn(b'Username must be atleast 5 characters.', response.data)

            # check if not redirected
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)

    def test_password_match(self):
        # simulate user input
        with self.client:
            response = self.client.post('/register', data=dict(
                username='testuser',
                password1='testpassword',
                password2='differentpassword'
            ), follow_redirects=True)

            # check if error message is displayed
            self.assertIn(b'Passwords do not match.', response.data)

            # check if not redirected
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)

    def test_password_length(self):
        # simulate user input
        with self.client:
            response = self.client.post('/register', data=dict(
                username='testuser',
                password1='tiny',
                password2='tiny'
            ), follow_redirects=True)

            # check if error message is displayed
            self.assertIn(b'Password must be atleast 5 characters.', response.data)

            # check if not redirected
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)

    
class TestCompleteReg(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.user = Userlogin(username='test_user', password='password', firstTime = False)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_completeReg_error_name(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="testuser", password="testpassword"
            ), follow_redirects=True)
            response = self.client.post('/complete', data=dict(
                fullname="John DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn Doe",
                address1="123 Main Street",
                address2="Apt 4B",
                city="New York",
                statedropdown="NY",
                zipcode="100"
            ), follow_redirects=True)
            self.assertIn('Full Name cannot be longer than 50 characters', response.data.decode())

    def test_completeReg_error_addr(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="testuser", password="testpassword"
            ), follow_redirects=True)
            response = self.client.post('/complete', data=dict(
                fullname="John",
                address1="123 Main Street John DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn Doe",
                address2="Apt 4B",
                city="New York",
                statedropdown="NY",
                zipcode="100"
            ), follow_redirects=True)
            self.assertIn('Address 1 cannot be longer than 100 characters', response.data.decode())
    
    def test_completeReg_error_addr2(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="testuser", password="testpassword"
            ), follow_redirects=True)
            response = self.client.post('/complete', data=dict(
                fullname="John",
                address1="123 Main Street",
                address2="Apt 4B 123 Main Street John DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn Doe",
                city="New York",
                statedropdown="NY",
                zipcode="100"
            ), follow_redirects=True)
            self.assertIn('Address 2 cannot be longer than 100 characters', response.data.decode())

    def test_completeReg_error_city(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="testuser", password="testpassword"
            ), follow_redirects=True)
            response = self.client.post('/complete', data=dict(
                fullname="John",
                address1="123 Main Street",
                address2="Apt 4B",
                city="New York 123 Main Street John DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn Doe",
                statedropdown="NY",
                zipcode="100"
            ), follow_redirects=True)
            self.assertIn('City cannot be longer than 100 characters', response.data.decode())

    def test_completeReg_error_zip2(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="testuser", password="testpassword"
            ), follow_redirects=True)
            response = self.client.post('/complete', data=dict(
                fullname="John",
                address1="123 Main Street",
                address2="Apt 4B",
                city="New York",
                statedropdown="NY",
                zipcode="1000001100"
            ), follow_redirects=True)
            self.assertIn('Zipcode cannot be longer than 9 characters', response.data.decode())

    def test_completeReg_error_zip1(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="testuser", password="testpassword"
            ), follow_redirects=True)
            response = self.client.post('/complete', data=dict(
                fullname="John",
                address1="123 Main Street",
                address2="Apt 4B",
                city="New York",
                statedropdown="NY",
                zipcode="100"
            ), follow_redirects=True)
            self.assertIn('Zipcode cannot be shorter than 5 characters', response.data.decode())

    def test_completeReg_success(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='test_user',
                password='password',
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='San Francisco',
                statedropdown='CA',
                zipcode='9410561'
            ), follow_redirects=True)

            
            self.assertEqual(response.status_code, 500)
if __name__ == '__main__':
    unittest.main()