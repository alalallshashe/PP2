import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(__file__)

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(os.path.join(BASE_DIR, filename))
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return config