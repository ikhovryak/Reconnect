import azure.cognitiveservices.speech as speechsdk

import wave
import contextlib

def get_correct_sound(filename, correct_text, speech_config):


    audio_output = speechsdk.AudioOutputConfig(filename=filename)


    # Creates a synthesizer with the given settings
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    correct_audio = speech_synthesizer.speak_text_async(correct_text).get()
    # Checks correct_audio.
    # if correct_audio.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     print("Speech synthesized to [{}] for correct_text [{}]".format(filename, correct_text))
    # elif correct_audio.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = correct_audio.cancellation_details
    #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         if cancellation_details.error_details:
    #             print("Error details: {}".format(cancellation_details.error_details))
    #     print("Did you update the subscription info?")
    return correct_audio

def get_audio_length(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
