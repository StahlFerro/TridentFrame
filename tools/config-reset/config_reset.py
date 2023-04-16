import shutil
from pathlib import Path

SCRIBE_PATH = Path(__file__).resolve()
PROJECT_DIR = SCRIBE_PATH.parents[2]
CONFIG_DIR = PROJECT_DIR.joinpath("config")

CONFIG_ORIG_FILE = CONFIG_DIR.joinpath("app-orig.toml")
CONFIG_FILE = CONFIG_DIR.joinpath("app.toml")

shutil.copyfile(CONFIG_ORIG_FILE, CONFIG_FILE)
