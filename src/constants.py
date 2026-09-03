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

CONFIG_DEFAULT = {
            'fullscreen_hide': True,
            'lmb_drag': False,
            'flip': False
        }

CONFIG_CONVERTER = {
            'fullscreen_hide': boolean,
            'lmb_drag': boolean,
            'flip': boolean,
        }

INIT_X = '-100'
INIT_Y = '-100'

FULLSCREEN_TOLERANCE = 5
VISIBILITY_POLL_INTERVAL = 100 # ms