class GraphicObject:
    def __init__(self, obj_type, name, coords):
        self.obj_type = obj_type  # "Ponto", "Linha", "Polilinha" ou "Polígono"
        self.name = name  # Nome do objeto
        self.coords = [(coord[0], coord[1], coord[2] if len(coord) > 2 else 0) for coord in coords]  # Coordenadas z com padrão 0

    def __repr__(self):
        return f"GraphicObject({self.name}, {self.obj_type}, {self.coords})"
