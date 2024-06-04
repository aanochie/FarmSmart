from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    Question = BooleanField(validators=[DataRequired()])
    Real_Answer = RadioField(validators=[DataRequired()])
    Fake_Answer_1 = RadioField(validators=[DataRequired()])
    Fake_Answer_2 = RadioField(validators=[DataRequired()])
    Fake_Answer_3 = RadioField(validators=[DataRequired()])
    Submit = SubmitField("Submit answer")
