from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Regexp

class QuizForm(FlaskForm):
    question = StringField('Question', validators=[InputRequired(), Regexp('^[\w]+$', message="Question must contain only alphanumeric letters")])
    answer1 = StringField('Answer 1', validators=[InputRequired(), Regexp('^[\w]+$', message="Question must contain only alphanumeric letters")])
    answer2 = StringField('Answer 2', validators=[InputRequired(), Regexp('^[\w]+$', message="Question must contain only alphanumeric letters")])
    answer3 = StringField('Answer 3', validators=[InputRequired(), Regexp('^[\w]+$', message="Question must contain only alphanumeric letters")])
    answer4 = StringField('Answer 4', validators=[InputRequired(), Regexp('^[\w]+$', message="Question must contain only alphanumeric letters")])
    answer = IntegerField('Correct Answer (1-4)', validators=[InputRequired(), Regexp('^\d{1}', message="Answer must be an integer of 1-4")])