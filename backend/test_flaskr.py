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
    
    def test_get_all_questions_return_an_object_containing_all_questions(self):
        res = self.client().get('/questions')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_body['success'], True)
        self.assertTrue(response_body['questions'])
        self.assertTrue(response_body['total_questions'])
        self.assertGreater(response_body['total_questions'], 0)
        self.assertTrue(response_body['categories'])
        self.assertIsNone(response_body['current_category'])
        
    def test_get_all_questions_return_404_if_page_number_is_out_of_range(self):
        res = self.client().get('/questions?page=1000')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_body['success'], False)
        self.assertEqual(response_body['message'], 'Resource Not Found')
        
    def test_delete_a_particular_question_then_that_question_does_not_exist_in_database_anymore(self):
        res = self.client().delete('/questions/2')
        response_body = json.loads(res.data)
        deleted_question = Question.query.filter(Question.id == 2).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_body['success'], True)
        self.assertEqual(response_body['deleted_question_id'], 2)
        self.assertIsNone(deleted_question)
    
    def test_delete_a_question_that_does_not_exist_in_database_then_return_404(self):
        res = self.client().delete('/questions/1000')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_body['success'], False)
        self.assertEqual(response_body['message'], 'Resource Not Found')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()