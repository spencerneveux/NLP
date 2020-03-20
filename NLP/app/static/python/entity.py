class Entity:
    def __init__(self):
        self.name: str = ""
        self.type: str = ""
        self.salience: float = 0.0

    # =========================
    # Getters
    # =========================
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_salience(self):
        return self.salience

    # =========================
    # Setters
    # =========================
    def set_name(self, name:str):
        self.name = name

    def set_type(self, type:str):
        self.type = type

    def set_salience(self, salience:float):
        self.salience = salience

    def __str__(self):
        return self.name + " - " + self.salience