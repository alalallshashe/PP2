from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)
    parser = ConfigParser()
    parser.read(filepath, encoding='utf-8')
    config = {}
    if parser.has_section(section):
        for param in parser.items(section):
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filepath}')
    return config
