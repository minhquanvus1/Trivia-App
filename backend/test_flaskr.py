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
        self.new_question = {"question": "Do you marry me?", "answer": "yes", "difficulty": 5, "category": 5}
        
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
    # -------Test for ['GET'] /categories endpoint-------
    def test_get_all_categories_return_an_object_containing_all_categories(self):
        res = self.client().get('/categories')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_body['success'], True)
        self.assertTrue(response_body['categories'])
        self.assertTrue(response_body['total_categories'])
        self.assertGreater(response_body['total_categories'], 0)
    #-------------------------------------------
    
    # -------Test for ['GET'] /questions endpoint-------
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
    #-------------------------------------------
    
    # -------Test for ['DELETE'] /questions/<int:question_id> endpoint-------
    
    def test_delete_a_particular_question_then_that_question_does_not_exist_in_database_anymore(self):
        res = self.client().delete('/questions/12')
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
    
    #-------------------------------------------
    
    # -------Test for ['POST'] /questions endpoint-------
    
    def test_POST_a_new_question_return_201_if_success(self):
        res = self.client().post('/questions', json=self.new_question)
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_body['success'], True)
        self.assertTrue(response_body['created_question_id'])
    
    def test_POST_a_new_question_return_400_if_question_is_empty(self):
        res = self.client().post('/questions', json={})
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_body['success'], False)
        self.assertEqual(response_body['message'], 'Bad Request')
    
    def test_POST_a_new_question_on_a_particular_question_resource_returns_405(self):
        res = self.client().post('/questions/1', json=self.new_question)
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(response_body['success'], False)
        self.assertEqual(response_body['message'], 'Method Not Allowed')
    
    #-------------------------------------------
    
    # -------Test for ['GET'] /categories/<int:category_id>/questions endpoint-------
    def test_get_questions_belong_to_a_particular_category_return_questions_of_that_category_and_their_total_number(self):
        res = self.client().get('/categories/1/questions')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_body['success'], True)
        self.assertTrue(response_body['questions'])
        self.assertTrue(response_body['total_questions'])
        self.assertGreaterEqual(response_body['total_questions'], 0)
        self.assertTrue(response_body['current_category'])
    
    def test_get_questions_belong_to_the_category_that_does_not_exist_return_422(self):
        res = self.client().get('/categories/1000/questions')
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(response_body['success'])
        self.assertEqual(response_body['message'], 'Unprocessable Entity')
    
    #-------------------------------------------
    
    # -------Test for ['POST'] /questions/search endpoint-------
    def test_search_for_questions_containing_search_term_returns_questions_containing_search_term(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'title'})
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_body['questions'])
        self.assertTrue(response_body['total_questions'])
        self.assertGreaterEqual(response_body['total_questions'], 0)
        self.assertIsNone(response_body['current_category'])
    
    def test_search_for_questions_containing_search_term_but_missing_search_term_in_the_request_returns_400(self):
        res = self.client().post('/questions/search', json={})
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(response_body['success'])
        self.assertEqual(response_body['message'], 'Bad Request')
    
    def test_search_for_questions_containing_search_term_but_search_term_is_empty_string_then_redirect_to_getQuestions_page(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})
        
        
        self.assertEqual(res.status_code, 302)
        
        self.assertIn('/questions', res.location)
    
    #-------------------------------------------
    
    # -------Test for ['POST'] /quizzes endpoint-------
    def test_get_question_to_play_quiz_given_No_previous_questions_and_quiz_category_is_Science_returns_current_question_of_category_Science(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1, 'type': 'Science'}})
        response_body = json.loads(res.data)
        if 'question' in response_body:
            
            # convert the question object from dictionary to Question object
            question_object = Question(**response_body['question'])
            category_of_current_question = Category.query.filter(Category.id == question_object.category).first().type
            
            self.assertEqual(res.status_code, 200)
            self.assertTrue(response_body['question'])
            self.assertIsInstance(response_body['question'], dict)
            self.assertIsInstance(question_object, Question)
            self.assertEqual(category_of_current_question, 'Science')
            self.assertTrue(question_object.id not in [])
    
    def test_get_question_to_play_quiz_given_previous_questions_with_id_1_and_quiz_category_is_All_returns_current_question_not_in_previous_questions_and_of_any_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [1,], 'quiz_category': {'id': 0, 'type': 'click'}})
        response_body = json.loads(res.data)
        if 'question' in response_body:
            
            # convert the question object from dictionary to Question object
            question_object = Question(**response_body['question'])
            category_of_current_question = Category.query.filter(Category.id == question_object.category).first().type
            
            self.assertEqual(res.status_code, 200)
            self.assertTrue(response_body['question'])
            self.assertIsInstance(response_body['question'], dict)
            self.assertIsInstance(question_object, Question)
            self.assertTrue(category_of_current_question in ['Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports'])
            self.assertTrue(question_object.id != 1)
    
    def test_get_question_to_play_quiz_without_sending_the_request_body_returns_400(self):
        res = self.client().post('/quizzes', json={})
        response_body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(response_body['success'])
        self.assertEqual(response_body['message'], 'Bad Request')
    #-------------------------------------------
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()