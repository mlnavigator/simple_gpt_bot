import json
import os
from threading import Lock

lock = Lock()

base_dir = os.path.dirname(os.path.abspath(__file__))

config_file_path = os.path.join(base_dir, 'assets/config.json')

config = {}

if config == {}:
    with lock:
        with open(config_file_path, 'r') as fd:
            config = json.load(fd)


def update_config_attribute(attribute, data):
    global config
    global lock
    config[str(attribute)] = str(data)
    with lock:
        with open(config_file_path, 'w') as fd:
            json.dump(config, fd)
