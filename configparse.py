import configparser
from typing import Union

class ConfigParse:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self._config_db = {
            'host' : config.get('Database', 'DB_HOST'),
            'port' : config.get('Database', 'DB_PORT'),
            'name' : config.get('Database', 'DB_NAME'),
            'user' : config.get('Database', 'DB_USER'),
            'password' : config.get('Database', 'DB_PASSWORD')
        }
    
    def get_config(self, key=None)-> Union[dict, str]:
        return self._config_db