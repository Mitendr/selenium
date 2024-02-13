
from configparser import ConfigParser


def read_config(section, key):
    config = ConfigParser()
    config.read("..//ConfigurationFile//conf.ini")
    try:
        value = config.get(section, key)
        return value
    except Exception as e:
        print(f"Error: {e}")
        return None





