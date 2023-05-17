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
        self.sound_dictionary = {} # keep a dictionary of common sounds
        self.status = 'silent' 
        self.frequency = None
        self.length = None
        wave_data = chr(128)
        self.sound_dictionary['silent'] = wave_data

        self.stream = self.pyaudio.open(
                format = self.pyaudio.get_format_from_width(1),
                channels = 2, rate = self.bitrate, output = True,
                stream_callback = self.callback)

        

    def __del__(self):
        """Tidy up on delete"""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        print (f"play ended, {frame_count}")
        wave_data = self.sound_dictionary.get(self.status, False)
        print(f'Got wave data {wave_data}')
        if not wave_data:
            number_frames = int(self.bitrate * self.length)
            rest_frames = number_frames % self.bitrate

            wave_data = ''

            for x in range(number_frames):
                wave_data = wave_data+chr(int(
                    math.sin(x/((self.bitrate/self.frequency)/math.pi))*127+128))

            for x in range(rest_frames):
                wave_data = wave_data+chr(128)

            self.sound_dictionary[dictname] = wave_data
        print(f'returning {wave_data}')
        return (wave_data, pyaudio.paContinue)


    def sound(self, length = 5, frequency = 10000):

        dictname = f"{length}_{frequency}"
        self.status = dictname
        self.length = length
        self.frequency = frequency
        self.stream.start_stream()
