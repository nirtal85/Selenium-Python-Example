import json
import os
from globals import dir_global


class JsonParser:
    def __init__(self, json_path):
        self.json_path = os.path.join(dir_global.DATA_FILES_PATH, json_path)

    def read_from_json(self):
        # read from file
        with open(self.json_path, 'r') as json_file:
            json_reader = json.load(json_file)
        return json_reader
