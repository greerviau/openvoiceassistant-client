import typing

import pyaudio
import sounddevice as sd


def find_devices(device_type: str) -> typing.Dict[int, typing.Dict]:
    if device_type not in ["input", "output"]:
        raise RuntimeError('Device kind must be "input" or "output"')
    devices = sd.query_devices()
    filtered = {}
    for i, _ in enumerate(devices):
        try:
            info = sd.query_devices(i, device_type)
            filtered[i] = info
        except ValueError:
            pass
    return filtered


def find_microphones() -> typing.Dict[int, typing.Dict]:
    return find_devices("input")


def find_speakers() -> typing.Dict[int, typing.Dict]:
    return find_devices("output")


def list_microphones() -> typing.List[str]:
    mics = find_microphones()
    mic_list = []
    for i, info in mics.items():
        mic_list.append({"name": info["name"], "idx": int(i)})
    return mic_list


def list_speakers() -> typing.List[str]:
    speakers = find_speakers()
    speaker_list = []
    for i, info in speakers.items():
        speaker_list.append({"name": info["name"], "idx": int(i)})
    return speaker_list


def select_mic(mic: typing.Union[str, int]) -> typing.Tuple[int, str]:
    microphones = find_microphones()
    try:
        if isinstance(mic, str):
            mic_index = [
                idx
                for idx, info in microphones.items()
                if mic.lower() in info["name"].lower()
            ][0]
        else:
            mic_index = mic

        mic_tag = microphones[mic_index]["name"]
    except Exception:
        raise RuntimeError("Microphone does not exist")

    return mic_index, mic_tag


def select_speaker(speaker: typing.Union[str, int]) -> typing.Tuple[int, str]:
    speakers = find_speakers()
    try:
        if isinstance(speaker, str):
            speaker_index = [
                idx
                for idx, info in speakers.items()
                if speaker.lower() in info["name"].lower()
            ][0]
        else:
            speaker_index = speaker

        speaker_tag = speakers[speaker_index]["name"]
    except Exception:
        raise RuntimeError("Speaker does not exist")

    return speaker_index, speaker_tag


def get_supported_samplerates(
    mic_index: int, samplerates: typing.List[int]
) -> typing.List[int]:
    paudio = pyaudio.PyAudio()
    supported_samplerates = []
    for fs in samplerates:
        try:
            if paudio.is_format_supported(
                fs,
                input_device=mic_index,
                input_channels=1,
                input_format=pyaudio.paInt16,
            ):
                supported_samplerates.append(fs)
        except ValueError:
            pass
    return supported_samplerates


def get_samplerate(mic_index: int) -> int:
    mic_info = sd.query_devices(mic_index, "input")
    samplerate = int(mic_info["default_samplerate"])
    return samplerate


def get_input_channels(mic_index: int) -> int:
    mic_info = sd.query_devices(mic_index, "input")
    channels = int(mic_info["max_input_channels"])
    return channels
