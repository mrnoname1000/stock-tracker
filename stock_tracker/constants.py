from pathlib import Path
from appdirs import AppDirs


PROGNAME = "stock-tracker"

_DIRS = AppDirs(PROGNAME)

DATA_DIR = Path(_DIRS.user_data_dir)
