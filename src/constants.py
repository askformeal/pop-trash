from pathlib import Path
from platformdirs import PlatformDirs

dirs = PlatformDirs('pop-trash', ensure_exists=True)
CONFIG_PATH = Path(dirs.user_data_dir) / 'config.toml'

def boolean(value):
    value = str(value).lower()
    if value in ('0', 'false'):
        return False
    elif value in ('1', 'true'):
        return True
    else:
        raise ValueError

def pos_int(value):
    value = int(value)
    if value <= 0:
        raise ValueError
    else:
        return value

CONFIG_DEFAULT = {
            'sound_effects': True,
            'fullscreen_hide': True,
            'lmb_drag': False,
            'flip': False,
            'temp_hide_time': 5,
        }

CONFIG_CONVERTER = {
            'sound_effects': boolean,
            'fullscreen_hide': boolean,
            'lmb_drag': boolean,
            'flip': boolean,
            'temp_hide_time': pos_int,
        }

INIT_X = '-100'
INIT_Y = '-100'

FULLSCREEN_TOLERANCE = 5
VISIBILITY_POLL_INTERVAL = 100 # ms