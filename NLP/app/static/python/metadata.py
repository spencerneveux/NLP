class Metadata:
    def __init__(self):
        self.key: str = ""
        self.value: str = ""

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def set_key(self, key:str):
        self.key = key

    def set_value(self, value:str):
        self.value = value

    def __str__(self):
        return f"{self.key} - {self.value}"