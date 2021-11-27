from pathlib import Path

import environ
import json

ROOT_DIR = Path(__file__).parents[1].absolute().resolve()

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(str(Path(ROOT_DIR, ".env")))

# False if not in os.environ
DEBUG = env("DEBUG")

# Telegram settings
TELEGRAM_API_TOKEN = env("TELEGRAM_API_TOKEN")
TELEGRAM_API_TOKEN_2 = env("TELEGRAM_API_TOKEN_2")

DATA_PATH = Path(env("DATA_PATH", default=Path(ROOT_DIR, "data")))

USER_FILE_PATH = Path(DATA_PATH, "users.json")

USERS_AVATAR_PATH = Path(DATA_PATH, "photos")

CONVERSATION_PATH = Path(ROOT_DIR / "osuc_companion" / "text")

CONVERSATIONS = json.load(Path(CONVERSATION_PATH / "replies.json").open())

GENDER_WORDS = {"El": "comodo", "Ella": "comoda", "Elle": "comode"}

MAINTAINER = "@Dyotson (Max Militzer)"
