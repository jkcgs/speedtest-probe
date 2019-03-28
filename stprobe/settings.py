import random

from ruamel import yaml
from os import path

from .logger import logger


def keygen(length=50):
    str_set = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(random.SystemRandom().choice(str_set) for _ in [0]*length)


read_only = True
_self_path = path.join(path.dirname(__file__), '..')
_defaults_path = path.join(_self_path, 'settings.example.yml')
_config_path = path.join(_self_path, 'settings.yml')

# Load default (example) settings file
with open(_defaults_path, 'r', encoding='utf8') as f:
    _defaults_content = f.read().format(very_secret=keygen())
    _defaults = yaml.safe_load(_defaults_content)

# Loading settings file (copy defaults or load current file)
if not path.exists(_config_path):
    logger.info('Configuration file does not exist, creating a new one...')
    with open(_config_path, 'w', encoding='utf8') as f:
        f.write(_defaults_content)
        _config = yaml.safe_load(_defaults_content)  # create a different object
        logger.info('New configuration file created',)
else:
    with open(_config_path, 'r', encoding='utf8') as f:
        cont = f.read()

    _config = {**_defaults, **yaml.safe_load(cont)}

logger.info('Configuration loaded from %s', _config_path)


def get(name):
    return _config[name]


# TODO: stub
def set_value(name, value):
    if read_only:
        return

    pass
