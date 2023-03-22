import pyaudio
import wave
import click

@click.command()
@click.option('--interval', '-i', default = 30, help='Length in milliseconds of each audio frame')
@click.option('--samplerate', '-sr', default = 16000, help='Samplerate of audio recording')
@click.option('--channels', '-c', default=1, help='Number of input channels')
@click.option('--durration', '-d', default=10, help='Recording durration in seconds')
@click.option('--output', '-o', default='recording.wav', help='Output file name')
@click.option('--mic_index', '-m', default=0, help='Index of the mic to record with')
@click.option('--list_mics', '-lm', is_flag=True, help='List microphones')
def main(interval, samplerate, channels, durration, output, mic_index, list_mics):
    if list_mics:
        import sounddevice as sd
        print(sd.query_devices())
        return

    FORMAT = pyaudio.paInt16

    CHUNK = int(samplerate * interval / 1000)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=channels,
                    input_device_index = mic_index,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print('Recording...')

    for i in range(0, int(samplerate / CHUNK * durration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()


    wf = wave.open(output, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(samplerate)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    main()