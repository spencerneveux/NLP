class Category:
    def __init__(self):
        self.name: str = ""
        self.confidence: float = 0.0

    def get_name(self):
        return self.name

    def get_confidence(self):
        return self.confidence

    def set_name(self, name:str):
        self.name = name

    def set_confidence(self, confidence:float):
        self.confidence = confidence

    def __str__(self):
        return f"{self.name} - {self.confidence}"

