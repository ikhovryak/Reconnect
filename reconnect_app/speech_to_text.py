import azure.cognitiveservices.speech as speechsdk

def get_text_from_input(input_audio_filename, speech_config):
    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_input = speechsdk.AudioConfig(filename=input_audio_filename)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    print("Recognizing first result...")


    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()
    # result = speech_recognizer.start_continuous_recognition()
    return result.text
