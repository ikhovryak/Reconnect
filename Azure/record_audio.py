
import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(correct_length):
    print("Start speaking...")
    fs = 44100  # Sample rate
    seconds = correct_length*1.5  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('input_sound.wav', fs, myrecording)  # Save as WAV file