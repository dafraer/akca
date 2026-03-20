from akca.db import store
import click

class App():
    def __init__(self, service: store.Store):
        print("Halo von App")
    def run(self):
        pass    