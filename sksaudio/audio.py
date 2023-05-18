#inspired by https://medium.com/py-bits/sound-generation-python-904e54f5398d
import math
import pyaudio


class sksaudio():
    """
    Maintains an audio stream to which we can subsequently 
    send sounds
    """
    def __init__(self):

        self.bitrate = 4410 #Hz
        self.pyaudio = pyaudio.PyAudio()
        self.sound_dictionary = {} # keep a dictionary of common sounds
        self.status = 'silent' 
        self.frequency = None
        self.length = None
        self.sound_buffer = ''
        self.counter = 0

        self.stream = self.pyaudio.open(
                format = self.pyaudio.get_format_from_width(1),
                channels = 2, rate = self.bitrate, output = True,
                stream_callback = self.callback)

        self.stream.start_stream()
        

    def __del__(self):
        """Tidy up on delete"""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        self.counter += 1
        if self.sound_buffer == '':
            print (f"Empty buffer, {self.counter}")
            wave_data = ''
            for _ in range (frame_count):
                wave_data = wave_data+chr(128)
        else:
            wave_data = self.sound_buffer[0:frame_count+1]
            self.sound_buffer = self.sound_buffer[frame_count+1:]
            #print(f'Got wave data {wave_data}')
            print (f"play ended, {frame_count}, {self.counter}")
            print (f'returning {len(wave_data)} {len(self.sound_buffer)}')
        #self.status = 'silent'
        return (wave_data, pyaudio.paContinue)


    def sound(self, length = 5, frequency = 10000):

        wave_data = self.sound_dictionary.get(self.status, False)
        if not wave_data:
            number_frames = int(self.bitrate * length)
            rest_frames = number_frames % self.bitrate

            wave_data = ''

            for x in range(number_frames):
                wave_data = wave_data+chr(int(
                    math.sin(x/((self.bitrate/frequency)/math.pi))*127+128))

            for x in range(rest_frames):
                wave_data = wave_data+chr(128)
            print(f'Adding {len(wave_data)} to sound buffer {len(self.sound_buffer)}')
            print(f'Stream active? {self.stream.is_active()}')
            if not self.stream.is_active():
                self.stream.start_stream()
            self.sound_buffer += wave_data

            self.sound_dictionary[self.status] = wave_data

        self.status = f"{length}_{frequency}"
        self.length = length
        self.frequency = frequency
