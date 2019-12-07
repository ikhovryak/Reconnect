import azure.cognitiveservices.speech as speechsdk
#import text_to_speech as t_t_s
from text_to_speech import get_correct_sound
from text_to_speech import get_audio_length
from record_audio import record_audio
from speech_to_text import get_text_from_input
# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "c87da06e1dfe4dd3b6e58fa41ec19c95", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

correct_audio_filename = "correct_sound.wav"
correct_text = "Hello world! Today is a beautiful day"

correct_audio = get_correct_sound(correct_audio_filename, correct_text, speech_config)
correct_length = get_audio_length(correct_audio_filename)

record_audio(correct_length)

input_audio_filename = "input_sound.wav"
input_text = get_text_from_input(input_audio_filename, speech_config)
print(input_text)



