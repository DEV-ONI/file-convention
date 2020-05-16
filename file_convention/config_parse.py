import toml
from pprint import pprint


def load_config(path):
    # required: target_directory
    config = toml.load(path)
    pprint(config)


load_config(TEST_PATH)
