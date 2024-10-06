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
                (x1, y1), (x2, y2) = obj.coords
                x1_vp, y1_vp = self.world_to_viewport(x1, y1)
                x2_vp, y2_vp = self.world_to_viewport(x2, y2)
                self.canvas.create_line(x1_vp, y1_vp, x2_vp, y2_vp, fill="black")
                self.canvas.create_text(x1_vp + 10, y1_vp, text=obj.name, anchor=tk.W)
            elif obj.obj_type == "Polilinha":
                for i in range(len(obj.coords) - 1):
                    x1, y1 = self.world_to_viewport(*obj.coords[i])
                    x2, y2 = self.world_to_viewport(*obj.coords[i + 1])
                    self.canvas.create_line(x1, y1, x2, y2, fill="black")
                self.canvas.create_text(x1 + 10, y1, text=obj.name, anchor=tk.W)
            elif obj.obj_type == "Polígono":
                points_vp = [self.world_to_viewport(x, y) for x, y in obj.coords]
                self.canvas.create_polygon(points_vp, outline="black", fill="", width=2)
                self.canvas.create_text(points_vp[0][0] + 10, points_vp[0][1], text=obj.name, anchor=tk.W)
