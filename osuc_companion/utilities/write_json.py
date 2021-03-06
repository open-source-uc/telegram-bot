import json
from pathlib import Path
from typing import Dict
from osuc_companion.settings import USER_FILE_PATH
from threading import Lock

# function to add to JSON
# TODO: Implementar que el bot detecte que existe el archivo
# TODO: Implementar que el bot detecte que el archivo no este corrupto
# TODO: Abrir y cerrar archivo


lock = Lock()


def write_json(new_data: Dict, filename: Path = USER_FILE_PATH):
    with lock:
        if not filename.exists():
            with filename.open("w") as file:
                json.dump([], file)
        with open(str(filename), "r+") as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data
            file_data.append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)
