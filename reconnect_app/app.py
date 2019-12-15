from flask import Flask, render_template, url_for, redirect, current_app, request
import azure.cognitiveservices.speech as speechsdk
from flask_sqlalchemy import SQLAlchemy
from text_to_speech import get_correct_sound
from text_to_speech import get_audio_length
import secrets
from scipy.io.wavfile import write
from forms import CorrectSpeechForm, UserSpeechForm
import os.path
from os import path
import time
from werkzeug import secure_filename
# from record_audio import record_audio
from speech_to_text import get_text_from_input
from compare_text import *
import glob


app = Flask(__name__)
speech_key, service_region = "c87da06e1dfe4dd3b6e58fa41ec19c95", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
app.config['SECRET_KEY'] = "4cf9c9881c554ef032f3a12c7f225dea"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Speech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correct_text = db.Column(db.String())
    correct_audio_filename = db.Column(db.String())
    # correct_audio = db.Column(None)
    # user_audio = db.Column(None)
    user_audio_location = db.Column(db.String())
    user_text = db.Column(db.String())
    def __repr__(self):
        return f"Speech('{self.id}', '{self.correct_text}', '{self.correct_audio_filename}')"

data = {
    "correct_text": "This app doesn't work",
    "path": "D:/Haverford/LocalHack/speech_analysis/reconnect_app/static/CorrectSounds/",
    "correct_audio_filename": "correct_sound",
    "user_audio_filename" : "user_sound"

}


def generate_user_text(user_audio_path):
    # new_file_name = str(time.time()) +  user_audio_filename + str(time.time()) + ".wav"
    path_to_file = os.path.join(app.root_path, "static/Sounds", user_audio_path)
    text = get_text_from_input(path_to_file, speech_config)
    return text

def save_sound_file(user_audio):
    random_hex = secrets.token_hex(6)
    _, f_ext = os.path.splitext(user_audio.filename)
    audio_fn = "input_sound" + random_hex + f_ext
    audio_path = os.path.join(app.root_path, 'static/Sounds', audio_fn)
    user_audio.save(audio_path)
    return audio_fn

def generate_correct_sound(correct_text):
    new_file_name = data["correct_audio_filename"] + secrets.token_hex(6) + ".wav"
    print(new_file_name)
    path_to_file = os.path.join(app.root_path, "static/Sounds", new_file_name)
    correct_audio = get_correct_sound(path_to_file, correct_text, speech_config)
    return "static/Sounds/" + new_file_name

@app.route("/")
def home():

    return render_template('index.html', title="Reconnect - Main")

@app.route("/learn", methods=["GET", "POST"])
def learn():

    correct_form = CorrectSpeechForm()
    if correct_form.submitc.data and correct_form.validate_on_submit():
        user_form = UserSpeechForm()
        print(correct_form.correct_text.data)
        correct_sound_address = generate_correct_sound(correct_form.correct_text.data)
        correct_audio = open(correct_sound_address)
        speech = Speech(correct_text=correct_form.correct_text.data, correct_audio_filename=correct_sound_address)
        print("from learn -> ", speech)
        db.session.add(speech)
        db.session.commit()
        return redirect(url_for('practice2'))

    return render_template('learn.html', correct_form=correct_form, title="Learn - Reconnect")

@app.route("/practice", methods=["GET", "POST"])
def practice():
    user_form = UserSpeechForm()
    correct_form = CorrectSpeechForm()
    speech = Speech.query.order_by(-Speech.id).first()

    print("we got to practice route")
    print(speech)
    #doesn't validate the form?? doesn't get into next lines
    if user_form.submitu.data and user_form.validate_on_submit():
        print("Got the sound!")
        filename = secure_filename(user_form.user_speech.data.filename)
        user_form.user_speech.data.save('static/Sounds/' + filename)
        speech.user_audio_location = 'static/Sounds/' + filename
        speech.user_text = generate_user_text(speech.user_audio_location)
        db.session.commit()
        return url_for('feedback', speech=speech)
    return render_template('practice.html', correct_text=speech.correct_text, correct_form=correct_form, user_form=user_form, correct_sound_address=str(speech.correct_audio_filename), title="Practice - Reconnect")

@app.route("/practice2", methods=["GET", "POST"])
def practice2():
    user_form = UserSpeechForm()
    speech = Speech.query.order_by(-Speech.id).first()

    print("we got to practice2 route")
    print(speech)
    #doesn't validate the form?? doesn't get into next lines
    if user_form.validate_on_submit():
        print("Got the sound!")
        filename = save_sound_file(user_form.user_speech.data)
        print("Filename -> ", filename)

        speech.user_audio_location = "static/Sounds/" + filename
        print("Location in db -> ", speech.user_audio_location )
        speech.user_text = generate_user_text(filename)
        print("Recognized text -> ", speech.user_text)
        db.session.commit()
        return redirect(url_for('feedback'))
    return render_template('practice2.html', correct_text=speech.correct_text, user_form=user_form, correct_sound_address=str(speech.correct_audio_filename), title="Practice - Reconnect")


@app.route("/feedback")
def feedback():
    speech = Speech.query.order_by(-Speech.id).first()
    # differences = get_differences(speech.correct_text, speech.user_text)
    # print(differences)
    correct_list = list_of_words(clean(speech.correct_text))

    user_list = list_of_words(clean(speech.user_text))
    # wrong_correct = differences.keys()
    # wrong_user = differences.values()
    wrong_correct, wrong_user = get_differences(speech.correct_text, speech.user_text)
    if len(correct_list)>=len(user_list):
        threshold = len(user_list)//2
    else:
        threshold = len(correct_list)//2
    print("wrong_correct -> ", wrong_correct)
    print("wrong_user -> ", wrong_user)
    return render_template('feedback.html', threshold=threshold, correct_list=correct_list, user_list=user_list, wrong_correct=wrong_correct, wrong_user=wrong_user, title="Reconnect - Feedback")

@app.route("/restart")
def restart():
    AUDIO_FOLDER = glob.glob(os.path.join(app.root_path, 'static/Sounds/*'))
    for f in AUDIO_FOLDER:
        os.remove(f)
    return redirect(url_for('learn'))

if __name__ == '__main__':
    app.run(debug=True)
