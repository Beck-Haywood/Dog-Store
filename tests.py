# tests.py

from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app


class DogStoreTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""
            

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_index(self):
        """Test the DOGSTORE homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Dog Store', result.data)
    
    def test_new(self):
        """Test the new DOGSTORE creation page."""
        result = self.client.get('/sell')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Dog', result.data)

        
if __name__ == '__main__':
    unittest_main()

