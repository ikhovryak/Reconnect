from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CorrectSpeechForm(FlaskForm):
    correct_text = TextField('Type in the sentence you want to practice today:', validators=[DataRequired()])
    submitc = SubmitField('Generate correct sound')


class UserSpeechForm(FlaskForm):
    user_speech = FileField('Your recording', validators=[FileAllowed(['wav']), FileRequired()])
    submitu = SubmitField('Submit recording')
