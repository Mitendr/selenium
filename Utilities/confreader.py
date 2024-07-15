from configparser import ConfigParser
import os


def read_config(section, key):
    config = ConfigParser()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    file_path = os.path.join(parent_dir, "ConfigurationFile", "conf.ini")
    config.read(file_path)
    try:
        value = config.get(section, key)
        return value
    except Exception as e:
        print(f"Error: {e}")
        return None



