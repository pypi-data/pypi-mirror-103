from os.path import exists
from pathlib import Path

import yaml
from yaml import CLoader as Loader, CDumper as Dumper


class YAML:
    path = None
    data = {}

    def __init__(self, yaml_file_path):
        self.path = yaml_file_path

        if not exists(self.path):
            Path(self.path).touch()

    def load(self):
        if not exists(self.path):
            return None

        with open(self.path) as file:
            return yaml.load(file.read(), Loader=Loader)

    def add(self, data):
        self.data = {**self.data, **data}

    def write(self):
        yml = yaml.dump(self.data, Dumper=Dumper)

        with open(self.path, 'w') as file:
            file.write(yml)
