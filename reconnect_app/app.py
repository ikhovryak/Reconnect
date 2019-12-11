from flask import Flask, render_template, url_for, redirect, current_app
import azure.cognitiveservices.speech as speechsdk
from flask_sqlalchemy import SQLAlchemy
from text_to_speech import get_correct_sound
from text_to_speech import get_audio_length
#import sounddevice as sd
from scipy.io.wavfile import write
from forms import CorrectSpeechForm, UserSpeechForm
import os.path
from os import path
import time

# from record_audio import record_audio
from speech_to_text import get_text_from_input
# from compare_text import *

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

def get_file_name(filename):
    if filename[0]=="1":
        return filename[1:]
    else:
        return filename.split(".")[-1]+ "1" + filename.split(".")[-1]

def generate_user_text(user_audio_filename):
    new_file_name = str(time.time()) +  data["user_audio_filename"] + str(time.time()) + ".wav"
    path_to_file = os.path.join(app.root_path, "static/Sounds", new_file_name)
    return get_text_from_input(path_to_file, speech_config)

def generate_correct_sound(correct_text):
    new_file_name = data["correct_audio_filename"] + str(time.time()) + ".wav"
    print(new_file_name)
    path_to_file = os.path.join(app.root_path, "static/Sounds", new_file_name)
    if path.exists("static/Sounds/*"):
        os.remove("static/Sounds/*")
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
        return redirect(url_for('practice'))

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
        speech.user_audio_location = user_form.user_speech.data.name
        speech.user_text = generate_user_text(user_form.user_speech.data.name)
        db.session.commit()
        return url_for('feedback', speech=speech)
    return render_template('practice.html', correct_text=speech.correct_text, correct_form=correct_form, user_form=user_form, correct_sound_address=str(speech.correct_audio_filename), title="Practice - Reconnect")




def learn2():
    if speech:
        user_form = UserSpeechForm()
        if user_form.validate_on_submit():
            print("Got the sound!")
            user_text = generate_user_text(user_form.user_speech.data.name)
            speech.user_audio = user_form.user_speech
            speech.user_text = user_text
            db.session.commit()
    return render_template('learn.html', correct_form=correct_form, title="Learn - Reconnect", correct_text = correct_form.correct_text.data,  speech=speech, correct_sound_address=correct_sound_address)


@app.route("/feedback")
def feedback():

    return render_template('feedback.html')


if __name__ == '__main__':
    app.run(debug=True)
