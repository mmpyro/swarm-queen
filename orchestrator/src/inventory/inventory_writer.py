class InventoryWriter(object):

    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.file_name = file_name

    def save(self, inventory: str) -> None:
        with open(self.file_name, 'w') as file:
            file.write(inventory)