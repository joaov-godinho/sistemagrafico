# graphic_object.py

class GraphicObject:
    def __init__(self, obj_type, name, coords):
        self.obj_type = obj_type  # "Ponto", "Linha", "Polilinha" ou "Polígono"
        self.name = name  # Nome do objeto
        self.coords = coords  # Coordenadas do objeto
