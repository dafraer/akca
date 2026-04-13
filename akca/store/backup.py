import shutil
from datetime import date



def backup(self, directory: str):
    shutil.copyfile(self.path, f"{directory}/backup{date.today()}.db")
