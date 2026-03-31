import click

def create(self, name: str, currency: str) -> int:
    try: 
        self.store.create_account(name, currency) 
    except:
        pass  

def edit(self, id: int, name: str, currency: str) -> int:
    self.store.edit_account(id, name, currency) 


def delete(self, id: int) -> int:
    self.store.delete_account(id)


def list(self) -> list[tuple]:
    return self.store.list_accounts();