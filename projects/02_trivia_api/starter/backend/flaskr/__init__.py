#!/usr/bin/python3.7.7
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def retrieve_categories():
#Front end requires a dictionary (object) for categories.
    categories = {}
    for c in Category.query.all():
      categories[c.id] = c.type
    if len(categories) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'categories': categories
    })

  '''
  @TODO: 
  
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  #Create function to paginate the questions
  questions_per_page = 10
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    if page:
      start =  (page - 1) * questions_per_page
    else:
      start = 0  
    end = start + questions_per_page
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions
  #GET is for the paginated display of questions; POST is to add a new question. 
  @app.route('/questions', methods =["GET","POST"])
  def retrieve_questions():
    if request.method=="GET":
      categories = {}
      for c in Category.query.all():
        categories[c.id] = c.type
      selection = Question.query.all()
      current_questions = paginate_questions(request, selection)

      if len(current_questions) == 0:
        abort(404)
      
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'categories': categories,
        'current_category': 1
      })
    else:
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
          question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty,category=new_category)
          question.insert()
          return jsonify({
            'success': True,
            'created': question.id,
            'total_questions': len(Question.query.all())
          })

        except:
          abort(422) 

  
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:id>', methods = ["DELETE"])
  def delete_question(id):
    try:
      selection = Question.query.filter_by(id=id).first()
      if selection is None:
          abort(404)
      selection.delete()    
      return jsonify({
        'success': True,
        'deleted': id,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)  

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # see above (included in 'questions' endpoint in POST request)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods = ["POST"])
  def search_for_books():
    body = request.get_json()
    searchTerm = body.get('searchTerm', None)
    question_matches = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
    questions = [question.format() for question in question_matches]
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(questions),
      'current_category':1
    })



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def get_questions_by_category(cat_id):
    questions_by_category = Question.query.filter(Question.category==cat_id).all()
    questions = [question.format() for question in questions_by_category]
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(questions),
      'current_category':cat_id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ["POST"])
  def play_game():
    body = request.get_json()
    prev = body.get('previous_questions', None)
    category = body.get('quiz_category', None)
    #Account for user selecting "ALL"
    if category==0:
      questions_by_category = Question.query.all()
    else:  
      questions_by_category = Question.query.filter(Question.category==category).all()
    questions = [question.format() for question in questions_by_category]
    if len(questions)==0:
      abort(422)
    else:  
      unasked_questions=[]
      for question in questions:
        if question['id'] not in prev:
          unasked_questions.append(question)
      #Choose a question randomly from questions list.    
      number = len(unasked_questions)
      question_num=random.randrange(number)
      question=unasked_questions[question_num]
      return jsonify({
        'success':True,
        'question':question
      })    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(405)
  def bad_method(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "wrong method"
      }), 405
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 405
  return app

    