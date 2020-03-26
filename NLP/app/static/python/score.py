class Score:
    def __init__(self):
        self.score: float = 0.0
        self.magnitude: float = 0.0

    def get_score(self):
        return self.score

    def get_magnitude(self):
        return self.magnitude

    def set_score(self, score:float):
        self.score = score

    def set_magnitude(self, magnitude:float):
        self.magnitude = magnitude

    def __str__(self):
        return f"{self.score} - {self.magnitude}"