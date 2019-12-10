from flask import Flask, render_template, url_for, redirect
import azure.cognitiveservices.speech as speechsdk
# #import text_to_speech as t_t_s
from text_to_speech import get_correct_sound
from text_to_speech import get_audio_length
import sounddevice as sd
from scipy.io.wavfile import write
# from record_audio import record_audio
# from speech_to_text import get_text_from_input
# from compare_text import *
app = Flask(__name__)
speech_key, service_region = "c87da06e1dfe4dd3b6e58fa41ec19c95", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
data = {
    "correct_text": "Hello! I love my cat and my dog",
    "path": "D:/Haverford/LocalHack/speech_analysis/reconnect_app/static/Sounds/",
    "correct_audio_filename": "correct_sound.wav"
}

def generate_correct_sound(correct_text):
    correct_text = correct_text
    path_to_file = data["path"] + data["correct_audio_filename"]
    correct_audio = get_correct_sound(path_to_file, correct_text, speech_config)
    return data["correct_audio_filename"]

@app.route("/")
@app.route("/learn")
def home():
    correct_sound_address = generate_correct_sound(data["correct_text"])

    return render_template('index.html', correct_sound_address=correct_sound_address, cor_str=data["correct_text"])




@app.route("/feedback")
def start():

    #
    #correct_audio_filename = "/static/correct_sound.wav"
    #correct_text = data["correct_text"]
    #
    # correct_audio = get_correct_sound(correct_audio_filename, correct_text, speech_config)
    # correct_length = get_audio_length(correct_audio_filename)
    #
    # input_audio_filename = "input_sound.wav"
    # input_text = get_text_from_input(input_audio_filename, speech_config)
    #
    # differences = compare(correct_text, input_text)
    # difs_og = keys(differences)
    # difs_new = values(differences)
    #
    # spl_og = correct_text.split(" ")
    # spl_new = input_text.split(" ")
    # if(is_empty(differences)):
    #     difs_og = None
    #     difs_new = None
    # return render_template('index2.html', cor_str=data["correct_text"], input_text=input_text, difs_og=difs_og, difs_new=difs_new, spl_og=spl_og, spl_new=spl_new)
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)
