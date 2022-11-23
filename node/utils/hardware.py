from typing import List, Dict, Tuple, Union

import sounddevice as sd

def find_devices(kind) -> List[Dict]:
    if kind not in ['input', 'output']:
        raise RuntimeError('Device kind must be \"input\" or \"output\"')
    devices = sd.query_devices()
    mics = []
    for i, device in enumerate(devices):
        try:
            info = sd.query_devices(i, kind)
            mics.append(device)
        except ValueError:
            pass
    return mics

def find_microphones() -> List[Dict]:
    return find_devices('input')

def find_speakers() -> List[Dict]:
    return find_devices('output')

def list_microphones() -> List[str]:
    mics = find_microphones()
    mic_list = []
    for i, info in enumerate(mics):
        name = info['name']
        mic_list.append(f'{i}: {name}')
    return mic_list

def list_speakers() -> List[str]:
    mics = find_speakers()
    mic_list = []
    for i, info in enumerate(mics):
        name = info['name']
        mic_list.append(f'{i}: {name}')
    return mic_list

def select_mic(mic: Union[str, int]) -> Tuple[int, str]:
    microphones = list_microphones()
    try:
        if isinstance(mic, str):
            mic_index = [idx for idx, element in enumerate(microphones) if mic in element.lower()][0]
        else:
            mic_index = mic
        
        mic_tag = microphones[mic_index]
    except:
        return 0, ''
        
    return mic_index, mic_tag

def get_samplerate(mic_index: int) -> int:
    mic_info = sd.query_devices(mic_index, 'input')
    samplerate = int(mic_info['default_samplerate'])
    return samplerate

def get_input_channels(mic_index: int) -> int:
    mic_info = sd.query_devices(mic_index, 'input')
    channels = int(mic_info['max_input_channels'])
    return channels