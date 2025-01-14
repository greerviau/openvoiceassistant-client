import wave

import pyaudio
import webrtcvad

vad = webrtcvad.Vad()
vad.set_mode(3)

INTERVAL = 30
RATE = 48000
CHUNK = int(RATE * INTERVAL / 1000)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    print("Is Speech ", vad.is_speech(data, RATE))
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()


wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()
