# viewport.py

import tkinter as tk

class Viewport:
    def __init__(self, canvas, world_x_min, world_x_max, world_y_min, world_y_max):
        self.canvas = canvas
        self.world_x_min = world_x_min
        self.world_x_max = world_x_max
        self.world_y_min = world_y_min
        self.world_y_max = world_y_max

    # Função de transformação de coordenadas do mundo para o viewport
    def world_to_viewport(self, x, y):
        self.canvas.update_idletasks()  # Garante que o canvas está atualizado
        viewport_width = self.canvas.winfo_width()
        viewport_height = self.canvas.winfo_height()

        viewport_x = ((x - self.world_x_min) / (self.world_x_max - self.world_x_min)) * viewport_width
        viewport_y = viewport_height - ((y - self.world_y_min) / (self.world_y_max - self.world_y_min)) * viewport_height

        return viewport_x, viewport_y

    # Função para atualizar o conteúdo do canvas
    def update_canvas(self, display_list):
        self.canvas.delete("all")  # Limpar o canvas
        for obj in display_list:
            if obj.obj_type == "Ponto":
                x, y = self.world_to_viewport(*obj.coords[0])
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
                self.canvas.create_text(x + 10, y, text=obj.name, anchor=tk.W)
            elif obj.obj_type == "Linha":
                if len(obj.coords) >= 2:
                    (x1, y1), (x2, y2) = obj.coords[:2]
                    x1_vp, y1_vp = self.world_to_viewport(x1, y1)
                    x2_vp, y2_vp = self.world_to_viewport(x2, y2)
                    self.canvas.create_line(x1_vp, y1_vp, x2_vp, y2_vp, fill="black")
                    self.canvas.create_text(x1_vp + 10, y1_vp, text=obj.name, anchor=tk.W)
            elif obj.obj_type == "Polilinha":
                if len(obj.coords) >= 2:
                    points_vp = []
                    for (x, y) in obj.coords:
                        x_vp, y_vp = self.world_to_viewport(x, y)
                        points_vp.extend([x_vp, y_vp])
                    self.canvas.create_line(*points_vp, fill="black")
                    self.canvas.create_text(points_vp[0] + 10, points_vp[1], text=obj.name, anchor=tk.W)
            elif obj.obj_type == "Polígono":
                if len(obj.coords) >= 3:
                    points_vp = []
                    for (x, y) in obj.coords:
                        x_vp, y_vp = self.world_to_viewport(x, y)
                        points_vp.extend([x_vp, y_vp])
                    self.canvas.create_polygon(*points_vp, outline="black", fill="", width=2)
                    self.canvas.create_text(points_vp[0] + 10, points_vp[1], text=obj.name, anchor=tk.W)