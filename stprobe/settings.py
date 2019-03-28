from ruamel import yaml
from os import path

from .logger import logger

_defaults_content = """\
# Interval in minutes
scan-interval: 2
# List of servers
servers:
- 17307 # Grupo GTD - Valdivia
- 939   # Telefónica Chile - Santiago
- 1779  # Comcast - Miami
"""

_defaults = yaml.safe_load(_defaults_content)
read_only = True
config_path = path.abspath(path.join(path.dirname(__file__), '..', 'settings.yml'))

if not path.exists(config_path):
    logger.info('Configuration file does not exist, creating a new one...')
    with open(config_path, 'w', encoding='utf8') as f:
        f.write(_defaults_content)
        _config = yaml.safe_load(_defaults_content)  # create a different object
        logger.info('New configuration file created at %s', config_path)
else:
    with open(config_path, 'r', encoding='utf8') as f:
        cont = f.read()

    _config = {**_defaults, **yaml.safe_load(cont)}
    logger.info('Configuration loaded.')


def get(name):
    return _config[name]


# TODO: stub
def set_value(name, value):
    if read_only:
        return

    pass
