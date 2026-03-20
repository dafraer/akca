from akca.db import store
import click

class App():
    def __init__(self, service: store.Store):
        print("Halo aus App")
    def run(self):
        pass    