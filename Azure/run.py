import azure.cognitiveservices.speech as speechsdk
#import text_to_speech as t_t_s
from text_to_speech import get_correct_sound
from text_to_speech import get_audio_length
from record_audio import record_audio
from speech_to_text import get_text_from_input
from compare_text import *
# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "c87da06e1dfe4dd3b6e58fa41ec19c95", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
correct_audio_filename = "correct_sound.wav"
print("Enter a phrase you want to practice today:")
correct_text = input()

prGreen(correct_text)

correct_audio = get_correct_sound(correct_audio_filename, correct_text, speech_config)
correct_length = get_audio_length(correct_audio_filename)

record_audio(correct_length)

input_audio_filename = "input_sound.wav"
input_text = get_text_from_input(input_audio_filename, speech_config)
prGreen(input_text)


remove_these_words = ["a", "um", "uh", "ah", "umm", "oh"]
got_text = input_text.lower()
expected_text = correct_text.lower()
expected_list = list_of_words(clean(expected_text))
got_list = list_of_words(clean(got_text))
refined_expected_list = remove_words(remove_these_words, expected_list)
refined_got_list = remove_words(remove_these_words, got_list)
diffs = compare(refined_expected_list, refined_got_list)

print("These are some words you mispronounced:")
prGreen(diffs)



