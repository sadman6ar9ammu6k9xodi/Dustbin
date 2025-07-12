import unittest
import tempfile
import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Paste

class DustbinTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_homepage(self):
        """Test homepage loads correctly"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome to Dustbin', rv.data)
    
    def test_new_paste_page(self):
        """Test new paste page loads"""
        rv = self.app.get('/new')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Create New Paste', rv.data)
    
    def test_create_paste(self):
        """Test creating a new paste"""
        rv = self.app.post('/new', data={
            'title': 'Test Paste',
            'content': 'print("Hello, World!")',
            'language': 'python',
            'expires_in': 'never',
            'is_public': True
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Test Paste', rv.data)
    
    def test_user_registration(self):
        """Test user registration"""
        rv = self.app.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Registration successful', rv.data)
    
    def test_user_login(self):
        """Test user login"""
        # First create a user
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
        
        # Then try to login
        rv = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Logged in successfully', rv.data)
    
    def test_paste_model(self):
        """Test paste model functionality"""
        with app.app_context():
            paste = Paste(
                title='Test Paste',
                content='print("Hello")',
                language='python'
            )
            db.session.add(paste)
            db.session.commit()
            
            # Test that paste was created with an ID
            self.assertIsNotNone(paste.id)
            self.assertEqual(len(paste.id), 8)
            
            # Test syntax highlighting
            highlighted = paste.get_highlighted_content()
            self.assertIn('highlight', highlighted)
    
    def test_search_functionality(self):
        """Test search functionality"""
        # Create a test paste first
        with app.app_context():
            paste = Paste(
                title='Python Example',
                content='def hello(): print("world")',
                language='python',
                is_public=True
            )
            db.session.add(paste)
            db.session.commit()
        
        # Search for it
        rv = self.app.get('/search?q=Python')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Python Example', rv.data)
    
    def test_api_endpoint(self):
        """Test API endpoint"""
        # Create a test paste
        with app.app_context():
            paste = Paste(
                title='API Test',
                content='console.log("test")',
                language='javascript',
                is_public=True
            )
            db.session.add(paste)
            db.session.commit()
            paste_id = paste.id
        
        # Test API endpoint
        rv = self.app.get(f'/api/paste/{paste_id}')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.content_type, 'application/json')

if __name__ == '__main__':
    unittest.main()
