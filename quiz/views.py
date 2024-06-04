import random

from flask import Blueprint, render_template, request
from dbSetup import Question
from quiz.form import QuizForm
from app import login_required
# Written by: Steven (c2045361)
quiz_blueprint = Blueprint('quiz', __name__, template_folder='templates')

global maxid
maxid = 1
# Use a global variable to track the current question ID
global currentqid
currentqid = random.randint(1, maxid)


@quiz_blueprint.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    global currentqid
    # Determine the maximum question ID in the database
    findmaxid()
    # Generate a form for the current question ID
    form = quizform(currentqid)
    # Render the quiz.html template with the form
    return render_template('quiz/quiz.html', form=form)


@quiz_blueprint.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    global currentqid
    form = quizform(currentqid)
    # Retrieve the answer submitted by the user from the form
    answer = request.form.get('Answer')
    # Compare the submitted answer with the correct answer
    if answer == 'Real':
        success = True
    else:
        success = False
    # Render the quiz.html template with the results displayed
    return render_template('quiz/quiz.html', results=True, success=success)


@quiz_blueprint.route('/retry', methods=['GET', 'POST'])
@login_required
def retry():
    global currentqid
    form = quizform(currentqid)
    # Render the quiz.html template to allow the user to retry the quiz
    return render_template('quiz/quiz.html', form=form)


@quiz_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    global currentqid
    # Randomly select a new question ID between 1 and 6
    currentqid = random.randint(1, 6)
    # Generate a form for the new question ID
    form = quizform(currentqid)
    # Render the quiz.html template with the new form
    return render_template('quiz/quiz.html', form=form)


def quizform(qid):
    # Create a new instance of the QuizForm
    form = QuizForm()
    # Query the database for the question with the given ID
    question = Question.query.filter_by(QID=qid).first()
    # Populate the form with the question and answers from the database
    form.Question = question.question
    form.Real_Answer = question.real_answer
    form.Fake_Answer_1 = question.fake_answer_1
    form.Fake_Answer_2 = question.fake_answer_2
    form.Fake_Answer_3 = question.fake_answer_3
    # Return the populated form
    return form


def findmaxid():
    # Use a global variable to track the maximum question ID
    global maxid
    maxid = 0
    # Iterate through all questions in the database and count them
    for i in Question.query.filter_by():
        maxid = maxid + 1
    # Return the maximum question ID
    return maxid
