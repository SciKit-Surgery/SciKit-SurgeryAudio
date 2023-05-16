#inspired by https://medium.com/py-bits/sound-generation-python-904e54f5398d
import math
import pyaudio


class sksaudio():
    """
    Maintains an audio stream to which we can subsequently 
    send sounds
    """
    def __init__(self):

        self.bitrate = 44100 #Hz
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(
                format = self.pyaudio.get_format_from_width(1),
                channels = 2, rate = self.bitrate, output = True)


    def __del__(self):
        """Tidy up on delete"""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()


    def sound(self, length = 5, frequency = 10000):

        number_frames = int(self.bitrate * length)
        rest_frames = number_frames % self.bitrate

        wave_data = ''

        for x in range(number_frames):
            wave_data = wave_data+chr(int(
                math.sin(x/((self.bitrate/frequency)/math.pi))*127+128))

        for x in range(rest_frames):
            wave_data = wave_data+chr(128)

        self.stream.write(wave_data)
