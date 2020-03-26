from google.cloud.language_v1 import enums
from .knowledge import Knowledge
from .metadata import Metadata

class Entity:
    def __init__(self):
        self.name: str = ""
        self.type: str = ""
        self.salience: float = 0.0
        self.knowledge: [Knowledge] = []
        self.metadata: [Metadata] = []

    # =========================
    # Getters
    # =========================
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_salience(self):
        return self.salience

    def get_knowledge(self):
        return self.knowledge

    def get_metadata(self):
        return self.metadata

    # =========================
    # Setters
    # =========================
    def set_name(self, name:str):
        self.name = name

    def set_type(self, type:str):
        self.type = enums.Entity.Type(type).name

    def set_salience(self, salience:float):
        self.salience = salience

    def set_knowledge(self, knowledge:Knowledge):
        self.knowledge.append(knowledge)

    def set_metadata(self, metadata:Metadata):
        self.metadata.append(metadata)

    def __str__(self):
        return f"{self.name} - {self.salience} - {self.type}"