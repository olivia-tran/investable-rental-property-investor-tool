import unittest
from server import app
from model import db, connect_to_db, example_data

# test data is called example_data()
# test db is called "postgresql:///testdb"


class FlaskTests(unittest.TestCase):
    '''Tests for non-logged in users'''

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')
        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_homepage(self):
        '''Test non-user will be prompted to register and not able to save property analysis'''
        result = self.client.get('/')
        self.assertIn(b'REGISTER FOR FREE', result.data)
        self.assertNotIn(b'Click here to save property data', result.data)

    def test_login_landing_page(self):
        '''Test login landing page'''
        result = self.client.get('/login')
        self.assertIn(b"Sign in", result.data)

    def test_register(self):
        '''Test register page'''
        result = self.client.get(
            '/register')
        self.assertIn(b"Already have an account?", result.data)

    def tearDown(self):
        '''Do at end of every test'''
        db.session.close()
        db.drop_all()


class TestsDatabase(unittest.TestCase):
    '''Flask tests that use the database for logged-in users'''

    def setUp(self):
        '''Things to do before every test'''

        # Get the flask test client
        self.client = app.test_client()
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'yoda@gmail.com'
        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')
        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        '''Do at end of every test'''
        db.session.close()
        db.drop_all()

    def test_profile(self):
        '''Test user's profile page'''
        result = self.client.get('/profile')
        self.assertIn(b'User Stats', result.data)

    def test_login(self):
        '''Test login page'''
        result = self.client.post(
            '/login', data={'email': 'yoda@gmail.com', 'password': '123456'}, follow_redirects=True)
        self.assertIn(b"You're signed in using:", result.data)

    def test_register_user(self):
        '''Test register user function'''
        result = self.client.post(
            '/login', data={'first': 'Baby', 'last': 'Yoda', 'email': 'yoda@gmail.com', 'password': '123456'}, follow_redirects=True)
        self.assertIn(b"No properties found!", result.data)

    def test_forum(self):
        '''Test forum page'''
        result = self.client.get(
            '/forum')
        self.assertIn(b"Create a Post", result.data)

    def test_property_page(self):
        '''Test property page'''
        result = self.client.get(
            '/properties')
        self.assertIn(b"You\'re signed in using", result.data)

    def test_blog_post(self):
        '''Test user's creating a blog post'''
        result = self.client.get('/blogging')
        self.assertIn(b'Blog Content', result.data)

    def test_posting_a_blog(self):
        '''Test if a user can post a blog'''
        content = {'title': 'This is to test the posting func',
                   'blog_content': 'Posting something to test'}
        result = self.client.post(
            '/blogging', data=content, follow_redirects=True)
        self.assertIn(b'Content Preview', result.data)

    def test_update_profile(self):
        '''Test if a user can update their profile'''
        result = self.client.get(
            '/profile/1')
        self.assertIn(b'Update User Info', result.data)

    def test_contact_route(self):
        '''Test if a user can go to contact route'''
        result = self.client.get(
            '/contact')
        self.assertIn(b"love to hear from you!", result.data)

    def test_logout(self):
        '''Test logout route'''
        with self.client as c:
            with c.session_transaction() as session:
                session['email'] = 'yoda@gmail.com'
            result = self.client.get('/logout', follow_redirects=True)
            self.assertNotIn(b'email', session)
            self.assertIn(b'LOGIN', result.data)


if __name__ == "__main__":
    unittest.main()
