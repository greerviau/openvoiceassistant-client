
import time
import collections
import webrtcvad

from node.wake import KaldiWake
from node.utils.audio import *
from node import config


class Listener:
    def __init__(self, 
                 node: 'Node',
                 wake_word: str, 
                 device_idx: int, 
                 sample_rate: int, 
                 sample_width: int,
                 channels: int,
                 sensitivity: int,
    ):
        self.node = node
        self.wake_word = wake_word
        self.device_idx = device_idx
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.channels = channels
        self.sensitivity = sensitivity
        self.wakeup_sound = config.get('wakeup', 'wakeup_sound')

        # Define a recording buffer for the start of the recording
        self.recording_buffer = collections.deque(maxlen=2)
        
        self.wake = KaldiWake(wake_word=self.wake_word,
                              sample_rate=self.sample_rate)
        
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(sensitivity)

        self.vad_chunk_size = 960 # 30ms
        self.vad_audio_data = bytes()

        self.engaged_delay = 3 # 5sec
    
    def listen(self, engaged: bool=False):
        self.node.stream.reset()
        audio_data = []
        if not engaged:
            self.wake.listen_for_wake_word(self.node.stream)

        self.node.pause_flag.set()
        
        if self.wakeup_sound:
            self.node.audio_player.play_audio_file('node/sounds/activate.wav')
            #audio_data = [chunk for chunk in self.stream.recording_buffer]

        # Capture ~0.5 seconds of audio
        for _ in range(20):
            chunk = self.node.stream.get_chunk()
            audio_data.append(chunk)

        start = time.time()

        while True:
            chunk = self.node.stream.get_chunk()

            if chunk:

                audio_data.append(chunk)

                with io.BytesIO() as wav_buffer:
                    wav_file: wave.Wave_write = wave.open(wav_buffer, "wb")
                    with wav_file:
                        wav_file.setframerate(self.sample_rate)
                        wav_file.setsampwidth(self.sample_width)
                        wav_file.setnchannels(self.channels)
                        wav_file.writeframes(chunk)

                    wav_bytes = wav_buffer.getvalue()

                    self.vad_audio_data += maybe_convert_wav(wav_bytes, sample_rate=16000, sample_width=2, channels=1)

                    is_speech = False

                    # Process in chunks of 30ms for webrtcvad
                    while len(self.vad_audio_data) >= self.vad_chunk_size:
                        vad_chunk = self.vad_audio_data[: self.vad_chunk_size]
                        self.vad_audio_data = self.vad_audio_data[self.vad_chunk_size:]

                        # Speech in any chunk counts as speech
                        is_speech = is_speech or self.vad.is_speech(vad_chunk, 16000)

                        if engaged and time.time() - start < self.engaged_delay:    # If we are engaged, wait at least 5 seconds to hear something
                            is_speech = True

                    if not is_speech:
                        # Capture ~0.5 seconds of audio
                        for _ in range(10):
                            chunk = self.node.stream.get_chunk()
                            audio_data.append(chunk)
                        if self.wakeup_sound:
                            self.node.audio_player.play_audio_file('node/sounds/deactivate.wav', asynchronous=True)
                        return b''.join(audio_data)