import tomllib
import tomli_w

from src.constants import CONFIG_CONVERTER, CONFIG_DEFAULT, CONFIG_PATH

class Config:
    def __init__(self):
        self.config = {}

        self.load()

    def load(self):
        try:
            with open(CONFIG_PATH, 'rb') as f:
                file_config = tomllib.load(f)
        except OSError:
            file_config = {}

        self.config = CONFIG_DEFAULT.copy()
        for name, value in file_config.items():
            self._set_option(name, value)

    def save(self):
        tmp_path = CONFIG_PATH.with_suffix('.tmp')
        with open(tmp_path, 'wb') as f:
            tomli_w.dump(self.config, f)
        tmp_path.replace(CONFIG_PATH)

    def _set_option(self, name, value):
        if name in CONFIG_DEFAULT.keys():
            try:
                value = CONFIG_CONVERTER[name](value)
            except ValueError:
                ...
            else:
                self.config[name] = value

    def __getattr__(self, name):
        try:
            return self.config[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name, value):
        if name in CONFIG_DEFAULT.keys():
            self.config[name] = value
            self.save()
        else:
            object.__setattr__(self, name, value)

CONFIG = Config()