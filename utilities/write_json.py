import json
from telegram.ext.dispatcher import run_async
# function to add to JSON
# TODO: Implementar que el bot detecte que existe el archivo
# TODO: Implementar que el bot detecte que el archivo no este corrupto
# TODO: Abrir y cerrar archivo

@run_async
def write_json(new_data, filename='users.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
