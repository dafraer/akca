from akca.db import store
from akca.cli import commands

class App():
    def __init__(self, service: store.Store):
        pass
    def run(self):
        commands.root()