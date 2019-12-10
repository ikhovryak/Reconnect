#required libraries
import math
import urllib.request
import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np

class SoundComparison:

    def compare_waves(self, speaker_sound, correct_sound):
        speaker_rate, pre_speaker_data = scipy.io.wavfile.read(speaker_sound)
        correct_rate, correct_data = scipy.io.wavfile.read(correct_sound)
        speaker_data = []
        for i in range(len(pre_speaker_data)):
            speaker_data.append((pre_speaker_data[i][0] + pre_speaker_data[i][1])/2)
        audio_data = [speaker_data, correct_data]
        audio_rate = [speaker_rate, correct_rate]
        # string = ""
        # for i in range(len(speaker_data)):
        #     string += str((speaker_data[i][0] + speaker_data[i][1])/2)
        #     string += "|"
        # print(string)
        # print(speaker_data
        #       )
        # print(len(speaker_data), speaker_rate)
        # print(len(correct_data), correct_rate)
        wave = self.normalize_audio_data_wave(speaker_data)
        speaker_data = self.remove_audio_wave_silent_start(wave, speaker_rate)
        wave = self.normalize_audio_data_wave(correct_data)
        correct_data = self.remove_audio_wave_silent_start(wave, correct_rate, 0)
        if self.check_for_long_breaks(speaker_data, speaker_rate) is not None:
            return False
        if self.check_for_amplitude_inconsistencies(speaker_data, speaker_rate, correct_data, correct_rate) is not None:
            return False
        return True

    def normalize_audio_data_wave(self, original_audio_data):
        final_audio_data = []
        for audio_data in original_audio_data:
            final_audio_data.append(abs(audio_data))
        max_amplitude = max(final_audio_data)
        for i in range(len(final_audio_data)):
            final_audio_data[i] = final_audio_data[i] / max_amplitude
        return final_audio_data

    def remove_audio_wave_silent_start(self, audio_data, rate, min=None):
        counter = 0
        while audio_data[counter] < self.calculate_silent_amplitude(audio_data, rate, min) or audio_data[counter] == 0:
            counter += 1
        return audio_data[counter:]

    def calculate_silent_amplitude(self, audio_data, rate, min=None):
        end = int(rate/3)
        return max(audio_data[:end]) if min is None else 0

    def check_for_long_breaks(self, audio_data, rate):
        counter = 0
        duration = 0
        while counter < len(audio_data):
            if audio_data[counter] < self.calculate_silent_amplitude(audio_data, rate):
                print("1")
                duration += 1
                if duration > (2.2 * rate):
                    return counter / rate
            else:
                duration = 0
                print("2", counter, len(audio_data))
            counter += 1
        return None

    def check_for_amplitude_inconsistencies(self, audio_data1, rate1, audio_data2, rate2):
        chunk_audio1 = self.convert_audio_data_to_chunk_audio_data(audio_data1, rate1)
        chunk_audio2 = self.convert_audio_data_to_chunk_audio_data(audio_data2, rate2)
        for i in range(len(chunk_audio1)):
            if abs(chunk_audio1[i] - chunk_audio2[i]) > 0.2:
                return i
        return None

    def convert_audio_data_to_chunk_audio_data(self, audio_data, rate):
        data = audio_data[:]
        chunk_audio_data = [0] * (data // (rate / 10) + 1)
        counter = 0
        for i in range(len(data)):
            chunk_audio_data[counter//(rate / 10)] += data[counter]
            counter += 1
        for i in range(len(chunk_audio_data)):
            chunk_audio_data[i] = chunk_audio_data[i] / (rate / 10)
        return chunk_audio_data

if __name__ == "__main__":
    # web_file="C:\Users\Samuel\PycharmProjects\speech_analysis\wave_comparison"
    #
    # #download file
    # input_sound, headers = urllib.request.urlretrieve("C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison", "input_sound")
    # correct_sound, headers = urllib.request.urlretrieve("C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison", "correct_sound")
    # wav_filename, headers = urllib.request.urlretrieve(web_file)
    # rate,audData=scipy.io.wavfile.read("C:\Users\Samuel\PycharmProjects\speech_analysis\wave_comparison")
    # time = np.arange(0, float(16000), 1) / rate
    # workable_data = []
    # string = ""
    # for data in audData[:16000]:
    #     workable_data.append(int(data))
    #     # string += str(data)
    #     # string += "."
    # # print(string)
    #
    # max = max(workable_data)
    #
    # happy = workable_data[:]
    # for i in range(len(happy)):
    #     happy[i] = abs(happy[i] / max)
    #     string += str(abs(happy[i] / max))
    #     string += "|"
    # print(happy[10400:15000])
    print(SoundComparison().compare_waves("C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison/input_sound.wav", "C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison/correct_sound.wav"))

