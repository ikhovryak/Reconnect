from flask_wtf import FlaskForm
from wtforms import TextField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CorrectSpeechForm(FlaskForm):
    correct_text = TextField('Type in the sentence you want to practice today:', validators=[DataRequired()])
    submitc = SubmitField('Generate correct sound')


class UserSpeechForm(FlaskForm):
    user_speech = FileField('Your recording', validators=[DataRequired()])
    submitu = SubmitField('Submit recording')
