import os, json

from functions import _get_vars


class State:
    def __init__(self, default=None, **kwargs):
        file, = _get_vars([
            ('file', 'STATE_FILE')
        ], kwargs)

        if default is None:
            default = {}

        self.file = file
        self.default = default

    def read(self) -> dict:
        if not os.path.exists(self.file):
            self.write(self.default)
            return self.default

        with open(self.file, 'r') as f:
            return json.loads(f.read())

    def write(self, state: dict):
        with open(self.file, 'w') as f:
            f.write(json.dumps(state))