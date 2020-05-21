import toml
from pprint import pprint


def load_config(path):
    config = toml.load(path)
    conventions_map = {convention['target_directory']: convention for convention in config}

    return conventions_map
