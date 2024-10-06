# graphic_system.py

import tkinter as tk
from input_window import InputWindow
from viewport import Viewport

class GraphicSystem:
    def __init__(self, root):
        self.root = root
        self.display_list = []
        self.viewport = Viewport(tk.Canvas(root, width=500, height=500, bg="white"), -250, 250, -250, 250)

        self.init_ui()

    def init_ui(self):
        self.viewport.canvas.pack(side=tk.LEFT)

        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.btn_add_point = tk.Button(self.control_panel, text="Adicionar Ponto", command=self.add_point)
        self.btn_add_point.pack(pady=10)

        self.btn_add_line = tk.Button(self.control_panel, text="Adicionar Linha", command=self.add_line)
        self.btn_add_line.pack(pady=10)

        self.btn_add_polyline = tk.Button(self.control_panel, text="Adicionar Polilinha", command=self.add_polyline)
        self.btn_add_polyline.pack(pady=10)

        self.btn_add_polygon = tk.Button(self.control_panel, text="Adicionar Polígono", command=self.add_polygon)
        self.btn_add_polygon.pack(pady=10)

        # Botões de navegação
        self.btn_up = tk.Button(self.control_panel, text="Mover Para Cima", command=lambda: self.pan_window(0, 50))
        self.btn_up.pack(pady=5)

        self.btn_down = tk.Button(self.control_panel, text="Mover Para Baixo", command=lambda: self.pan_window(0, -50))
        self.btn_down.pack(pady=5)

        self.btn_left = tk.Button(self.control_panel, text="Mover Para Esquerda", command=lambda: self.pan_window(-50, 0))
        self.btn_left.pack(pady=5)

        self.btn_right = tk.Button(self.control_panel, text="Mover Para Direita", command=lambda: self.pan_window(50, 0))
        self.btn_right.pack(pady=5)

        # Botões de zoom
        self.btn_zoom_in = tk.Button(self.control_panel, text="Zoom In", command=lambda: self.zoom(0.9))
        self.btn_zoom_in.pack(pady=5)

        self.btn_zoom_out = tk.Button(self.control_panel, text="Zoom Out", command=lambda: self.zoom(1.1))
        self.btn_zoom_out.pack(pady=5)

        self.btn_remove = tk.Button(self.control_panel, text="Remover Objeto", command=self.remove_object)
        self.btn_remove.pack(pady=10)

        self.update_viewport()

    def add_point(self):
        InputWindow(self.root, "Ponto", is_line=False, is_polyline=False, display_list=self.display_list, update_viewport=self.update_viewport)

    def add_line(self):
        InputWindow(self.root, "Linha", is_line=True, is_polyline=False, display_list=self.display_list, update_viewport=self.update_viewport)

    def add_polyline(self):
        InputWindow(self.root, "Polilinha", is_line=False, is_polyline=True, display_list=self.display_list, update_viewport=self.update_viewport)

    def add_polygon(self):
        InputWindow(self.root, "Polígono", is_line=False, is_polyline=True, display_list=self.display_list, update_viewport=self.update_viewport)

    def pan_window(self, dx, dy):
        self.viewport.world_x_min += dx
        self.viewport.world_x_max += dx
        self.viewport.world_y_min += dy
        self.viewport.world_y_max += dy
        self.update_viewport()

    def zoom(self, factor):
        center_x = (self.viewport.world_x_min + self.viewport.world_x_max) / 2
        center_y = (self.viewport.world_y_min + self.viewport.world_y_max) / 2

        width = (self.viewport.world_x_max - self.viewport.world_x_min) * factor
        height = (self.viewport.world_y_max - self.viewport.world_y_min) * factor

        self.viewport.world_x_min = center_x - width / 2
        self.viewport.world_x_max = center_x + width / 2
        self.viewport.world_y_min = center_y - height / 2
        self.viewport.world_y_max = center_y + height / 2

        self.update_viewport()

    def update_viewport(self):
        self.viewport.update_canvas(self.display_list)

    def remove_object(self):
        name = simpledialog.askstring("Remover Objeto", "Digite o nome do objeto a ser removido:")
        self.display_list = [obj for obj in self.display_list if obj.name != name]
        self.update_viewport()
