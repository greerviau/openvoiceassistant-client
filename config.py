import os
import json
import typing

DEFAULT_CONFIG = {
    "node_id": "",
    "device_ip": "",
    "web_port": 0,
    "hub_ip": "",
    "hub_port": 0,
    "mic_tag": "",
    "mic_index": 0
}

class Configuration:
    def __init__(self):
        self.loc = os.path.realpath(os.path.dirname(__file__))
        self.config_path = f'{self.loc}/config.json'
        print(f'Loading config: {self.config_path}')
        self.config = {}
        self.load_config()

    def get(self, *keys: typing.List[str]):
        dic = self.config.copy()
        for key in keys:
            try:
                dic = dic[key]
            except KeyError:
                return None
        return dic

    def setkey(self, *keys: typing.List[str], value=None):
        if value is None:
            raise RuntimeError
        d = self.config
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value
        self.save_config()
        return value
        
    def config_exists(self):
        return os.path.exists(self.config_path)

    def save_config(self):
        print('Config saved')
        with open(self.config_path, 'w') as config_file:
            config_file.write(json.dumps(self.config, indent=4))

    def load_config(self) -> dict:  # TODO use TypedDict
        if not os.path.exists(self.config_path):
            print('Loading default config')
            self.config = DEFAULT_CONFIG
            self.save_config()
        else:
            print('Loading existing config')
            self.config = json.load(open(self.config_path, 'r'))