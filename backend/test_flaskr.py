import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_username = os.getenv('DB_USERNAME')
        self.database_password = os.getenv('DB_PASSWORD')
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(self.database_username, self.database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories_return_an_object_containing_all_categories(self):
        res = self.client().get('/categories')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_body['success'], True)
        self.assertTrue(response_body['categories'])
        self.assertTrue(response_body['total_categories'])
        self.assertGreater(response_body['total_categories'], 0)
        
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()