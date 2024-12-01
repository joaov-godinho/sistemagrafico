#graphic_system.py
import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, MULTIPLE, END, LabelFrame, Scrollbar, RIGHT, Y, BOTH
from viewport import Viewport
from transformations import apply_translation, apply_rotation, apply_scaling, apply_reflection, apply_shear
from transformation_window import TransformationWindow
from add_object_window import AddObjectWindow
from input_window import InputWindow
from polygon3d import Polygon3D


class GraphicSystem:
    def __init__(self, root):
        self.root = root
        self.display_list = []
        self.viewport = Viewport(tk.Canvas(root, width=500, height=500, bg="white"), -250, 250, -250, 250)
        self.init_ui()
        self.add_default_3d_object()  # Adiciona o objeto 3D ao iniciar

    def add_default_3d_object(self):
    # Exemplo de coordenadas 3D para um polígono
        coords = [
            (-25, -45, 0), (25, -45, 0), (25, 5, 0), (0, 45, 0),
            (-25, 5, 0), (-25, -45, 0), (-25, -45, -20), (25, -45, -20),
            (25, -45, 0), (25, -45, -20), (25, 5, -20), (25, 5, 0),
            (25, 5, -20), (0, 45, -20), (0, 45, 0), (0, 45, -20),
            (-25, 5, -20), (-25, 5, 0), (-25, 5, -20), (-25, -45, -20)
        ]
        polygon_3d = Polygon3D(coords, name="Casa 3D")  # Criação do objeto
        self.display_list.append(polygon_3d)  # Adiciona à lista de objetos para exibição
        self.update_listbox()  # Atualiza a lista de objetos no menu
        self.update_viewport()

    def draw_reference_axes(self):
        width = self.viewport.canvas.winfo_width()
        height = self.viewport.canvas.winfo_height()
        self.viewport.canvas.create_line(width // 2, 0, width // 2, height, fill="gray", dash=(4, 2))  # Linha do eixo Y
        self.viewport.canvas.create_line(0, height // 2, width, height // 2, fill="gray", dash=(4, 2))  # Linha do eixo X

    def init_ui(self):
        self.viewport.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Ajustar a viewport e desenhar os eixos após a renderização inicial
        self.root.after(100, self.update_viewport)

        # 1. Seção de Seleção de Objetos
        select_objects_frame = LabelFrame(self.control_panel, text="Selecionar Objetos", padx=10, pady=10)
        select_objects_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.object_listbox = Listbox(select_objects_frame, selectmode=MULTIPLE, width=30, height=10)
        self.object_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)

        scrollbar = Scrollbar(select_objects_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.object_listbox.yview)
        self.object_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 2. Botão de Adicionar Objetos
        self.btn_add_object = tk.Button(self.control_panel, text="Adicionar Objetos", width=20, command=self.open_add_object_menu)
        self.btn_add_object.pack(fill=tk.X, pady=5)

        # 3. Botão de Remover Objeto
        self.btn_remove = tk.Button(self.control_panel, text="Remover Objeto", width=20, command=self.remove_object)
        self.btn_remove.pack(fill=tk.X, pady=5)

        # 4. Botão de Transformações
        self.btn_transformations = tk.Button(self.control_panel, text="Transformações", width=20, command=self.open_transformations_menu)
        self.btn_transformations.pack(fill=tk.X, pady=5)

        # 5. Seção de Navegação
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

        # Zoom
        self.btn_zoom_in = tk.Button(navigation_frame, text="Zoom In", width=10, command=lambda: self.zoom(0.9))
        self.btn_zoom_in.grid(row=3, column=0, padx=5, pady=5)

        self.btn_zoom_out = tk.Button(navigation_frame, text="Zoom Out", width=10, command=lambda: self.zoom(1.1))
        self.btn_zoom_out.grid(row=3, column=2, padx=5, pady=5)

        self.update_viewport()

    def open_add_object_menu(self):
        # Menu para escolher o tipo de objeto a ser adicionado
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Adicionar Objeto")

        tk.Button(menu_window, text="Ponto", command=lambda: self.open_add_window("Ponto")).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(menu_window, text="Linha", command=lambda: self.open_add_window("Linha")).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(menu_window, text="Polilinha", command=lambda: self.open_add_window("Polilinha")).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(menu_window, text="Polígono", command=lambda: self.open_add_window("Polígono")).pack(fill=tk.X, pady=5, padx=10)

    def open_add_object_menu(self):
        from add_object_window import AddObjectWindow
        AddObjectWindow(self.root, self.display_list, self.update_viewport, self.update_listbox)


    def open_transformations_menu(self):
        from transformation_window import TransformationWindow
        selected_indices = self.object_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Nenhum objeto selecionado", "Por favor, selecione pelo menos um objeto para aplicar transformações.")
            return
        TransformationWindow(self.root, self.display_list, selected_indices, self.update_viewport)

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
        self.viewport.canvas.delete("all")
        self.viewport.update_canvas(self.display_list)
        self.draw_reference_axes()  # Garantir que os eixos são redesenhados

        for obj in self.display_list:
            if isinstance(obj, Polygon3D):
                # Projetando as coordenadas 3D para 2D (ignora Z e pega X, Y)
                for x, y, z in obj.coords:
                    screen_x, screen_y = self.viewport.world_to_viewport(x, y)
                    self.viewport.canvas.create_oval(screen_x - 3, screen_y - 3, screen_x + 3, screen_y + 3, fill="black")

    def remove_object(self):
        selected_indices = self.object_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum objeto selecionado para remoção.")
            return

        for index in reversed(selected_indices):  # Reverter para evitar problemas ao remover
            obj = self.display_list.pop(index)
            messagebox.showinfo("Removido", f"Objeto '{obj.name}' removido.")
        self.update_viewport()
        self.update_listbox()

    def apply_transformation(self, transformation_type):
        selected_indices = self.object_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum objeto selecionado para transformação.")
            return

        if transformation_type == "translation":
            dx, dy = map(float, simpledialog.askstring("Translação", "Digite dx e dy separados por vírgula:").split(','))
            for index in selected_indices:
                obj = self.display_list[index]
                obj.coords = apply_translation(obj.coords, dx, dy)

        elif transformation_type == "rotation":
            angle, (cx, cy) = self.get_rotation_inputs()
            for index in selected_indices:
                obj = self.display_list[index]
                obj.coords = apply_rotation(obj.coords, angle, (cx, cy))

        elif transformation_type == "scaling":
            scale_factor = float(simpledialog.askstring("Escalonamento", "Digite o fator de escala:"))
            for index in selected_indices:
                obj = self.display_list[index]
                obj.coords = apply_scaling(obj.coords, scale_factor)

        self.update_viewport()

    def get_rotation_inputs(self):
        angle = float(simpledialog.askstring("Ângulo", "Digite o ângulo de rotação em graus:"))
        cx, cy = map(float, simpledialog.askstring("Centro de Rotação", "Digite X e Y separados por vírgula:").split(','))
        return angle, (cx, cy)