# graphic_system.py

import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, MULTIPLE, END, LabelFrame, Scrollbar, RIGHT, Y, BOTH
import math
from input_window import InputWindow
from viewport import Viewport
import numpy as np


class GraphicSystem:
    def __init__(self, root):
        self.root = root
        self.display_list = []
        self.viewport = Viewport(tk.Canvas(root, width=500, height=500, bg="white"), -250, 250, -250, 250)
        self.init_ui()

    def init_ui(self):
        self.viewport.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # 1. Seção de Adicionar Objetos
        add_objects_frame = LabelFrame(self.control_panel, text="Adicionar Objetos", padx=10, pady=10)
        add_objects_frame.pack(fill=tk.X, pady=5)

        self.add_objects_expanded = True
        def toggle_add_objects():
            if self.add_objects_expanded:
                add_objects_frame.pack_forget()
                self.btn_toggle_add_objects.config(text="Expandir Adicionar Objetos")
            else:
                add_objects_frame.pack(fill=tk.X, pady=5)
                self.btn_toggle_add_objects.config(text="Recolher Adicionar Objetos")
            self.add_objects_expanded = not self.add_objects_expanded

        self.btn_toggle_add_objects = tk.Button(self.control_panel, text="Recolher Adicionar Objetos", command=toggle_add_objects)
        self.btn_toggle_add_objects.pack(fill=tk.X, pady=2)

        self.btn_add_point = tk.Button(add_objects_frame, text="Adicionar Ponto", width=20, command=self.add_point)
        self.btn_add_point.grid(row=0, column=0, padx=5, pady=5)

        self.btn_add_line = tk.Button(add_objects_frame, text="Adicionar Linha", width=20, command=self.add_line)
        self.btn_add_line.grid(row=1, column=0, padx=5, pady=5)

        self.btn_add_polyline = tk.Button(add_objects_frame, text="Adicionar Polilinha", width=20, command=self.add_polyline)
        self.btn_add_polyline.grid(row=2, column=0, padx=5, pady=5)

        self.btn_add_polygon = tk.Button(add_objects_frame, text="Adicionar Polígono", width=20, command=self.add_polygon)
        self.btn_add_polygon.grid(row=3, column=0, padx=5, pady=5)

        # 2. Seção de Seleção de Objetos
        select_objects_frame = LabelFrame(self.control_panel, text="Selecionar Objetos", padx=10, pady=10)
        select_objects_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.object_listbox = Listbox(select_objects_frame, selectmode=MULTIPLE, width=30, height=10)
        self.object_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5), pady=5)

        scrollbar = Scrollbar(select_objects_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.object_listbox.yview)
        self.object_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 3. Seção de Navegação
        navigation_frame = LabelFrame(self.control_panel, text="Navegação", padx=10, pady=10)
        navigation_frame.pack(fill=tk.X, pady=5)

        self.btn_up = tk.Button(navigation_frame, text="↑ Mover Para Cima", width=20, command=lambda: self.pan_window(0, 50))
        self.btn_up.grid(row=0, column=1, padx=5, pady=5)

        self.btn_down = tk.Button(navigation_frame, text="↓ Mover Para Baixo", width=20, command=lambda: self.pan_window(0, -50))
        self.btn_down.grid(row=2, column=1, padx=5, pady=5)

        self.btn_left = tk.Button(navigation_frame, text="← Mover Para Esquerda", width=20, command=lambda: self.pan_window(-50, 0))
        self.btn_left.grid(row=1, column=0, padx=5, pady=5)

        self.btn_right = tk.Button(navigation_frame, text="→ Mover Para Direita", width=20, command=lambda: self.pan_window(50, 0))
        self.btn_right.grid(row=1, column=2, padx=5, pady=5)

        # 4. Seção de Zoom
        zoom_frame = LabelFrame(self.control_panel, text="Zoom", padx=10, pady=10)
        zoom_frame.pack(fill=tk.X, pady=5)

        self.btn_zoom_in = tk.Button(zoom_frame, text="Zoom In", width=10, command=lambda: self.zoom(0.9))
        self.btn_zoom_in.grid(row=0, column=0, padx=5, pady=5)

        self.btn_zoom_out = tk.Button(zoom_frame, text="Zoom Out", width=10, command=lambda: self.zoom(1.1))
        self.btn_zoom_out.grid(row=0, column=1, padx=5, pady=5)

        # 5. Seção de Transformações
        transformations_frame = LabelFrame(self.control_panel, text="Transformações", padx=10, pady=10)
        transformations_frame.pack(fill=tk.X, pady=5)

        # Botão para recolher/expandir a seção de Transformações
        self.transformations_expanded = True
        def toggle_transformations():
            if self.transformations_expanded:
                transformations_frame.pack_forget()
                self.btn_toggle_transformations.config(text="Expandir Transformações")
            else:
                transformations_frame.pack(fill=tk.X, pady=5)
                self.btn_toggle_transformations.config(text="Recolher Transformações")
            self.transformations_expanded = not self.transformations_expanded

        self.btn_toggle_transformations = tk.Button(self.control_panel, text="Recolher Transformações", command=toggle_transformations)
        self.btn_toggle_transformations.pack(fill=tk.X, pady=2)

        # 5.1 Translação
        translation_frame = LabelFrame(transformations_frame, text="Translação", padx=10, pady=10)
        translation_frame.pack(fill=tk.X, pady=5)

        tk.Label(translation_frame, text="D_x:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.dx_entry = tk.Entry(translation_frame, width=10)
        self.dx_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(translation_frame, text="D_y:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.dy_entry = tk.Entry(translation_frame, width=10)
        self.dy_entry.grid(row=0, column=3, padx=5, pady=5)

        self.btn_translate = tk.Button(translation_frame, text="Aplicar Translação", width=20, command=self.apply_translation)
        self.btn_translate.grid(row=1, column=0, columnspan=4, pady=5)

        # 5.2 Rotação
        rotation_frame = LabelFrame(transformations_frame, text="Rotação", padx=10, pady=10)
        rotation_frame.pack(fill=tk.X, pady=5)

        tk.Label(rotation_frame, text="Ângulo (°):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.angle_entry = tk.Entry(rotation_frame, width=10)
        self.angle_entry.grid(row=0, column=1, padx=5, pady=5)

        self.btn_rotate = tk.Button(rotation_frame, text="Aplicar Rotação", width=20, command=self.apply_rotation)
        self.btn_rotate.grid(row=1, column=0, columnspan=2, pady=5)

        # 5.3 Escalonamento
        scaling_frame = LabelFrame(transformations_frame, text="Escalonamento", padx=10, pady=10)
        scaling_frame.pack(fill=tk.X, pady=5)

        tk.Label(scaling_frame, text="Fator:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.scale_entry = tk.Entry(scaling_frame, width=10)
        self.scale_entry.grid(row=0, column=1, padx=5, pady=5)

        self.btn_scale = tk.Button(scaling_frame, text="Aplicar Escalonamento", width=20, command=self.apply_scaling)
        self.btn_scale.grid(row=1, column=0, columnspan=2, pady=5)

        # 6. Seção de Remoção de Objeto
        remove_object_frame = LabelFrame(self.control_panel, text="Remoção de Objeto", padx=10, pady=10)
        remove_object_frame.pack(fill=tk.X, pady=5)

        self.btn_remove = tk.Button(remove_object_frame, text="Remover Objeto", width=20, command=self.remove_object)
        self.btn_remove.pack(pady=5)

        self.update_viewport()

    def add_point(self):
        InputWindow(self.root, "Ponto", is_line=False, is_polyline=False, display_list=self.display_list, update_viewport=self.update_viewport, update_listbox=self.update_listbox)

    def add_line(self):
        InputWindow(self.root, "Linha", is_line=True, is_polyline=False, display_list=self.display_list, update_viewport=self.update_viewport, update_listbox=self.update_listbox)

    def add_polyline(self):
        InputWindow(self.root, "Polilinha", is_line=False, is_polyline=True, display_list=self.display_list, update_viewport=self.update_viewport, update_listbox=self.update_listbox)

    def add_polygon(self):
        InputWindow(self.root, "Polígono", is_line=False, is_polyline=True, display_list=self.display_list, update_viewport=self.update_viewport, update_listbox=self.update_listbox)

    def update_listbox(self):
        self.object_listbox.delete(0, END)
        for obj in self.display_list:
            self.object_listbox.insert(END, obj.name)

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
        if name:
            original_length = len(self.display_list)
            self.display_list = [obj for obj in self.display_list if obj.name != name]
            if len(self.display_list) < original_length:
                messagebox.showinfo("Sucesso", f"Objeto '{name}' removido com sucesso.")
            else:
                messagebox.showwarning("Aviso", f"Nenhum objeto encontrado com o nome '{name}'.")
            self.update_viewport()
            self.update_listbox()

    # Funções de Transformação
    def apply_translation(self):
        try:
            dx = float(self.dx_entry.get())
            dy = float(self.dy_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Valores de translação inválidos.")
            return

        translation_matrix = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])

        selected_indices = self.object_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum objeto selecionado para translação.")
            return

        for index in selected_indices:
            obj = self.display_list[index]
            new_coords = [
                (translation_matrix.dot([x, y, 1])[:2]) for x, y in obj.coords
            ]
            obj.coords = new_coords
        self.update_viewport()

    def apply_rotation(self):
        try:
            angle_deg = float(self.angle_entry.get())
            cx, cy = map(float, simpledialog.askstring("Centro de Rotação", "Digite X e Y do ponto de rotação, separados por vírgula:").split(','))
        except (ValueError, AttributeError):
            messagebox.showerror("Erro", "Ângulo ou ponto de rotação inválido.")
            return

        angle_rad = math.radians(angle_deg)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        translation_to_origin = np.array([
            [1, 0, -cx],
            [0, 1, -cy],
            [0, 0, 1]
        ])
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])
        translation_back = np.array([
            [1, 0, cx],
            [0, 1, cy],
            [0, 0, 1]
        ])

        transformation_matrix = translation_back @ rotation_matrix @ translation_to_origin

        selected_indices = self.object_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum objeto selecionado para rotação.")
            return

        for index in selected_indices:
            obj = self.display_list[index]
            new_coords = [
                (transformation_matrix.dot([x, y, 1])[:2]) for x, y in obj.coords
            ]
            obj.coords = new_coords
        self.update_viewport()

    def apply_scaling(self):
        try:
            scale_factor = float(self.scale_entry.get())
            if scale_factor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Fator de escalonamento inválido. Deve ser um número positivo.")
            return

        selected_indices = self.object_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum objeto selecionado para escalonamento.")
            return

        for index in selected_indices:
            obj = self.display_list[index]
            base_x, base_y = obj.coords[0]  # Primeiro vértice como base
            translation_to_origin = np.array([
                [1, 0, -base_x],
                [0, 1, -base_y],
                [0, 0, 1]
            ])
            scaling_matrix = np.array([
                [scale_factor, 0, 0],
                [0, scale_factor, 0],
                [0, 0, 1]
            ])
            translation_back = np.array([
                [1, 0, base_x],
                [0, 1, base_y],
                [0, 0, 1]
            ])

            transformation_matrix = translation_back @ scaling_matrix @ translation_to_origin

            new_coords = [
                (transformation_matrix.dot([x, y, 1])[:2]) for x, y in obj.coords
            ]
            obj.coords = new_coords
        self.update_viewport()