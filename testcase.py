import unittest
from website import create_app, db
from flask import Flask, request, url_for,redirect
from website.models import Userlogin, User
from website.authenciation import completeReg
from website.pricing import pricing
from unittest.mock import patch
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

#test case for pricing module
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

#test case for login and logout
class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # create a test user
        self.user = Userlogin(username='testuser', password=generate_password_hash('testpass', method='sha256'), firstTime=True, hasHistory = False)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_success_firstTime(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='testpass',
            ), follow_redirects=True)

            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'testuser')

            if self.user.firstTime == True:
                self.assertIn(b'Please complete your registration', response.data)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Complete Registration', response.data)
            

            
    def test_login_success_notfirstTime(self):
        self.user.firstTime = False
        db.session.commit() 
        with self.client:
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='testpass',
            ), follow_redirects=True)

            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'testuser')

            #check if redirect to complete reg.
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Qoil', response.data)

    def test_username_notexist(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='notexist',
                password='testpass',
            ), follow_redirects=True)


            self.assertIn(b'Account does not exist.', response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data)
    
    def test_incorrectPass(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='wrongpass',
            ), follow_redirects=True)


            self.assertIn(b'Incorrect password, try again.', response.data)
                          
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data)

    def test_logout_firstTime(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='testpass'
            ), follow_redirects=True)

            # check that user is logged in
            self.assertTrue(current_user.is_authenticated)

            # log out the user
            response = self.client.get('/logout', follow_redirects=True)

            # check that user is logged out
            self.assertFalse(current_user.is_authenticated)

            # check that user is redirected to login page
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data)

    def test_logout_notfirstTime(self):
        self.user.firstTime = False
        db.session.commit()
        with self.client:
            response = self.client.post('/login', data=dict(
                username='testuser',
                password='testpass'
            ), follow_redirects=True)

            # check that user is logged in
            self.assertTrue(current_user.is_authenticated)

            # log out the user
            response = self.client.get('/logout', follow_redirects=True)

            # check that user is logged out
            self.assertFalse(current_user.is_authenticated)

            # check that user is redirected to login page
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data)

#test case for user registration
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

            #check if hasHistory variable for user is set to false
            self.assertFalse(user.hasHistory)

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

#test case for client complete registration
class TestCompleteReg(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.user = Userlogin(username='testuser', password=generate_password_hash('testpass', method='sha256'), firstTime=True)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_completeReg_error_name(self):
        with self.client:
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

            self.client.post('/login', data=dict(
                username='testuser',
                password='testpass'
            ), follow_redirects=True)

            response = self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='San Francisco',
                statedropdown='TX',
                zipcode='9410561'
            ), follow_redirects=True)

            myUser = Userlogin.query.filter_by(username = 'testuser').first()
            self.assertIsNotNone(myUser.userInfo)
            self.assertEqual(myUser.userInfo.fullname, 'Test User')
            self.assertEqual(myUser.userInfo.address, '123 Main St')
            self.assertEqual(myUser.userInfo.address2, '1234 main st')
            self.assertEqual(myUser.userInfo.state, 'TX')
            self.assertEqual(myUser.userInfo.zipcode, '9410561')

            self.assertFalse(self.user.firstTime)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Qoil', response.data)

#test case for fuel quote form
class test_form(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = Userlogin(username='testuser', password=generate_password_hash('testpass', method='sha256'), firstTime=False, hasHistory = False)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_with_firsttime(self):
        with self.client:
            response = self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass',
                firstTime = True
            ), follow_redirects=True)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, 'testuser')

            if self.user.firstTime == True:
                self.assertIn(b'Please complete your registration', response.data)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Complete Registration', response.data)


    def test_error_gal_amount(self):
        with self.client:

            self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)

            response = self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='San Francisco',
                statedropdown='TX',
                zipcode='9410561'
            ), follow_redirects=True)

            response = self.client.post('/form', data=dict(
                gallons_req = "something" 
            ), follow_redirects = True)
            
            

            self.assertIn(b'Number of gallons must be a valid integer', response.data)

    def form_success_noHistory(self):
        with self.client:
            self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)

            self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='San Francisco',
                statedropdown='TX',
                zipcode='9410561'
            ), follow_redirects=True)

            response = self.client.post('/form', data=dict(
                gallons_req = 1500,  
            ), follow_redirects = True)

            myUser = Userlogin.query.filter_by(username = 'testuser').first()
            self.assertIsNotNone(myUser.quotes)

            self.assertEqual(myUser.quotes.gallons_req, 1500)

            self.assertEqual(myUser.quotes.suggested_price, 1.71)
            self.assertEqual(myUser.quotes.total_amount, 2565)
        

            self.assertTrue(myUser.hasHistory)

            self.assertIn(b'Quote Requested!', response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Fuel Quote History Table', response.data)

    def form_success_History(self):
        with self.client:
            self.user.hasHistory = True
            self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)

            self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='San Francisco',
                statedropdown='TX',
                zipcode='9410561'
            ), follow_redirects=True)

            response = self.client.post('/form', data=dict(
                gallons_req = 1500,  
            ), follow_redirects = True)

            myUser = Userlogin.query.filter_by(username = 'testuser').first()
            self.assertIsNotNone(myUser.quotes)

            self.assertEqual(myUser.quotes.gallons_req, 1500)

            self.assertEqual(myUser.quotes.suggested_price, 1.695)
            self.assertEqual(myUser.quotes.total_amount, 2542.5)
        

            self.assertTrue(myUser.hasHistory)

            self.assertIn(b'Quote Requested!', response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Fuel Quote History Table', response.data)
    
    def getPrice(self):

        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
        
        self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='Dallas',
                statedropdown='TX',
                zipcode='9410561'
            ), follow_redirects=True)
        
        response = self.client.get(url_for('auth.get_price', gallons=100))

        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIn('suggested_price', data)
        self.assertIn('total_amount', data)

#test case for edit profile
class editProfile(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = Userlogin(username='testuser', password=generate_password_hash('testpass', method='sha256'), firstTime=False, hasHistory = False)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_profile_edit_fullname_too_long(self):
        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
 
        # Make a POST request to edit the profile with a fullname that's too long
        response = self.client.post('/edit', data={
            'fullnameE': 'This is a really long name that is more than fifty charactersThis is a really long name that is more than fifty characters',
            'address1E': '123 Main St',
            'address2E': '',
            'cityE': 'Anytown',
            'statedropdownE': 'CA',
            'zipcodeE': '12345'
        }, follow_redirects=True)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the appropriate error message was flashed
        self.assertIn(b'Full Name cannot be longer than 50 characters', response.data)

    def test_editprof_error_addr(self):
        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
            
        response = self.client.post('/edit', data={
            'fullnameE': 'This is a',
            'address1E': '123 Main St This is a really long name that is more than fifty charactersThis is a really long name that is more than fifty characters This is a really long name that is more than fifty charactersThis is a really long name that is more than fifty characters',
            'address2E': '',
            'cityE': 'Anytown',
            'statedropdownE': 'CA',
            'zipcodeE': '12345'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Address 1 cannot be longer than 100 characters', response.data)
    
    def test_editprof_error_addr2(self):
        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
            
        response = self.client.post('/edit', data={
            'fullnameE': 'This is a',
            'address1E': '123 Main St',
            'address2E': '123 Main St This is a really long name that is more than fifty charactersThis is a really long name that is more than fifty characters This is a really long name that is more than fifty charactersThis is a really long name that is more than fifty characters',
            'cityE': 'Anytown',
            'statedropdownE': 'CA',
            'zipcodeE': '12345'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Address 2 cannot be longer than 100 characters', response.data)

    def test_editprof_error_city(self):
        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
            
        self.client.post('/complete', data=dict(
                fullname='Test User',
                address1='123 Main St',
                address2='1234 main st',
                city='Dallas',
                statedropdown='TX',
                zipcode='9410561'
            ), follow_redirects=True)
        
        response = self.client.post('/edit', data={
            'fullnameE': 'This is a',
            'address1E': '123 Main St',
            'address2E': '1 This y characters',
            'cityE': 'New York 123 Main Street John DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn DoeJohn Doe',
            'statedropdownE': 'CA',
            'zipcodeE': '12345'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)    
        self.assertIn(b'City cannot be longer than 100 characters', response.data)

    def test_editprof_error_zip2(self):
        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
            
        response = self.client.post('/edit', data={
            'fullnameE': 'This is a',
            'address1E': '123 Main St',
            'address2E': '1 This y characters',
            'cityE': 'New York',
            'statedropdownE': 'CA',
            'zipcodeE': '12345567567'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)    
        self.assertIn(b'Zipcode cannot be longer than 9 characters', response.data)

    def test_editprof_error_zip1(self):
        self.client.post('/login', data = dict(
                username = 'testuser',
                password = 'testpass'
            ), follow_redirects=True)
            
        response = self.client.post('/edit', data={
            'fullnameE': 'This is a',
            'address1E': '123 Main St',
            'address2E': '1 This y characters',
            'cityE': 'New York',
            'statedropdownE': 'CA',
            'zipcodeE': '123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)    
        self.assertIn(b'Zipcode cannot be shorter than 5 characters', response.data)

    # def test_editprof_success(self):
    #     self.client.post('/login', data = dict(
    #             username = 'testuser',
    #             password = 'testpass'
    #         ), follow_redirects=True)
        
    #     response = self.client.post('/edit', data=dict(
    #             fullname='Test User',
    #             address1='123 Main St',
    #             address2='1234 main st',
    #             city='San Francisco',
    #             statedropdown='TX',
    #             zipcode='9410561'
    #         ), follow_redirects=True)
        
    #     response = self.client.post('/edit', data={
    #         'fullnameE': 'Test User',
    #         'address1E': '123 Main St',
    #         'address2E': '1234 main st',
    #         'cityE': 'San Francisco',
    #         'statedropdownE': 'TX',
    #         'zipcodeE': '9410561'
    #     }, follow_redirects=True)

    #     myUser = Userlogin.query.filter_by(username = 'testuser').first()
    #     self.assertIsNotNone(myUser.userInfo)
    #     self.assertEqual(myUser.userInfo.fullname, 'Test User')
    #     self.assertEqual(myUser.userInfo.address, '123 Main St')
    #     self.assertEqual(myUser.userInfo.address2, '1234 main st')
    #     self.assertEqual(myUser.userInfo.city, 'San Francisco')
    #     self.assertEqual(myUser.userInfo.state, 'TX')
    #     self.assertEqual(myUser.userInfo.zipcode, '9410561')

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Edit', response.data)

if __name__ == '__main__':
    unittest.main()