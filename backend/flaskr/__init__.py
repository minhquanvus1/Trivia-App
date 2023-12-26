import os
from flask import Flask, request, abort, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# define a helper function to return a list of questions on a particular page
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start_index = (page - 1) * QUESTIONS_PER_PAGE
    end_index = start_index + QUESTIONS_PER_PAGE
    list_of_questions_on_this_page = selection[start_index:end_index]
    # format the list of questions on this page, so that each question is a dictionary, and can be jsonifyed. 
    # Else, it will be a list of Question objects, which cannot be jsonifyed.
    return [question.format() for question in list_of_questions_on_this_page]

def convert_category_list_to_category_dict(list_of_categories):
    categories_in_dictionary = {category.id : category.type for category in list_of_categories}
    return categories_in_dictionary

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        return response
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        list_of_all_categories = Category.query.order_by(Category.id).all()
        if len(list_of_all_categories) == 0:
            abort(404)
        categories_in_dictionary = convert_category_list_to_category_dict(list_of_all_categories)
        return jsonify({
            'success': True,
            'categories': categories_in_dictionary,
            'total_categories': Category.query.count()
            }), 200

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        list_of_all_questions = Question.query.order_by(Question.id).all()
        list_of_questions_on_this_page = paginate_questions(request, list_of_all_questions)
        if len(list_of_questions_on_this_page) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': list_of_questions_on_this_page,
            'total_questions': Question.query.count(),
            'categories': convert_category_list_to_category_dict(Category.query.order_by(Category.id).all()),
            'current_category': None
            }), 200
        
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question_to_be_deleted = Question.query.filter(Question.id == id).one_or_none()
        if question_to_be_deleted is None:
            abort(404, description='Question with id {} not found'.format(id))
        question_to_be_deleted.delete()
        return jsonify({
            'success': True,
            'deleted_question_id': id
            }), 200
        
    
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_a_new_question():
        request_body = request.get_json()
        if request_body is None:
            abort(400, description='Request body is empty')
        question = request_body.get('question', None)
        answer = request_body.get('answer', None)
        category = request_body.get('category', None)
        difficulty = request_body.get('difficulty', None)
        if not all([question, answer, category, difficulty]):
            abort(400, description='One of the required fields is empty')
        new_question = Question(question=question, answer=answer, category=int(category), difficulty=int(difficulty))
        new_question.insert()
        return jsonify({
            'success': True,
            'created_question_id': new_question.id
            }), 201
        
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        request_body = request.get_json()
        # if searchTerm is NOT in the request body, then abort(400) BAD REQUEST
        if not 'searchTerm' in request_body:
            abort(400, description='Search term is not provided')
        
        search_term = request_body.get('searchTerm', '').strip()
        # if search term is empty, return all questions
        if search_term == '':
            return redirect(url_for('get_paginated_questions'))
        found_questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term))).all()
        
        if len(found_questions) == 0:
            # pass, because the frontend will handle the flash message
           pass
        
        return jsonify({
            'success': True,
            'questions': paginate_questions(request, found_questions),
            'total_questions': len(found_questions),
            'current_category': None
            }), 200
        
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_based_on_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
        if not category:
            abort(422, description='Category with id {} does not exist'.format(category_id))
        list_of_questions_belong_to_this_category = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
        return jsonify({
            'success': True,
            'questions': paginate_questions(request, list_of_questions_belong_to_this_category),
            'total_questions': len(list_of_questions_belong_to_this_category),
            'current_category': category_id
            }), 200
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_current_quiz_question():
        request_body = request.get_json()
        if not request_body:
            abort(400, description='Request body is empty')
        previous_questions = request_body.get('previous_questions', [])
        quiz_category = request_body.get('quiz_category', None)
        
        if quiz_category is None:
            abort(400, description='Quiz category is not provided')
            
        quiz_category_object = Category(**quiz_category)
        id_of_quiz_category = quiz_category_object.id
        type_of_quiz_category = quiz_category_object.type
        # id_of_quiz_category = quiz_category.get('id', 0)
        # type_of_quiz_category = quiz_category.get('type', 'click')
        
        
        if id_of_quiz_category == 0 and type_of_quiz_category == 'click':
            list_of_all_questions = Question.query.order_by(Question.id).all()
            # list_of_not_asked_questions = []
            # for question in list_of_all_questions:
            #     if question.id not in previous_questions:
            #         list_of_not_asked_questions.append(question)
            list_of_not_asked_questions = [question for question in list_of_all_questions if question.id not in previous_questions]
            if len(list_of_not_asked_questions) == 0:
                random_question = None
            else:
                random_question = random.choice(list_of_not_asked_questions)
        else:
            list_of_questions_belong_to_this_category = Question.query.filter(Question.category == id_of_quiz_category).all()
            list_of_not_asked_questions = [question for question in list_of_questions_belong_to_this_category if question.id not in previous_questions]
            # use Ternary operator to assign random_question to None if list_of_not_asked_questions is empty
            random_question = None if len(list_of_not_asked_questions) == 0 else random.choice(list_of_not_asked_questions)
            
            # this while loop will run forever if all questions have been asked.
            # random_question = random.choice(list_of_all_questions)
            # while random_question.id in previous_questions:
            #     random_question = random.choice(list_of_all_questions)
        
            
        return jsonify({
            'success': True,
            'question': random_question.format() if random_question else None
            }), 200
    
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
            }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
            }), 405
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
            }), 400
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
            }), 422
    return app

