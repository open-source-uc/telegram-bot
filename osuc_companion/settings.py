from pathlib import Path

import environ

ROOT_DIR = Path(__file__).parents[1].absolute().resolve()

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env(str(Path(ROOT_DIR, '.env')))

# False if not in os.environ
DEBUG = env('DEBUG')

# Telegram settings
TELEGRAM_API_TOKEN = env("TELEGRAM_API_TOKEN")
TELEGRAM_API_TOKEN_2 = env("TELEGRAM_API_TOKEN_2")

DATA_PATH = Path(
    env(
        "DATA_PATH",
        default=Path(ROOT_DIR, 'data')
        )
    )

USER_FILE_PATH = Path(DATA_PATH, 'users.json')

USERS_AVATAR_PATH = Path(
    DATA_PATH,
    'photos'
)
