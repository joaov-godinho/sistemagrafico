import tkinter as tk
from graphic_object import GraphicObject
from tkinter import Label, Entry, Button, Listbox, messagebox, ttk

class AddObjectWindow:
    def __init__(self, root, display_list, update_viewport, update_listbox):
        self.root = root
        self.display_list = display_list
        self.update_viewport = update_viewport
        self.update_listbox = update_listbox
        self.points = []
        self.init_window()

    def init_window(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Adicionar Objeto")

        # Nome do Objeto
        Label(self.add_window, text="Nome do Objeto:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry = Entry(self.add_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Display de Coordenadas Adicionadas
        Label(self.add_window, text="Coordenadas Adicionadas:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.coords_listbox = Listbox(self.add_window, height=5, width=50)
        self.coords_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Seletor do Tipo de Objeto
        Label(self.add_window, text="Tipo de Objeto:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.obj_type_selector = ttk.Combobox(self.add_window, values=["Ponto", "Linha", "Polilinha", "Polígono"])
        self.obj_type_selector.grid(row=3, column=1, padx=10, pady=5)
        self.obj_type_selector.bind("<<ComboboxSelected>>", self.update_fields)

        # Campos de Coordenadas (X, Y, Z)
        self.coord_label = Label(self.add_window, text="Coordenadas (X, Y, Z):")
        self.coord_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.coord_entry = Entry(self.add_window)
        self.coord_entry.grid(row=4, column=1, padx=10, pady=5)

        # Botões
        Button(self.add_window, text="Adicionar Coordenada", command=self.add_point).grid(row=5, column=0, columnspan=2, pady=5)
        Button(self.add_window, text="Finalizar Objeto", command=self.finish_object).grid(row=6, column=0, columnspan=2, pady=5)

    def update_fields(self, event):
        obj_type = self.obj_type_selector.get()
        if obj_type == "Linha":
            self.coord_label.config(text="Coordenadas (X1, Y1, Z1), (X2, Y2, Z2):")
        elif obj_type in ["Polilinha", "Polígono"]:
            self.coord_label.config(text="Coordenadas (X, Y, Z):")
        else:
            self.coord_label.config(text="Coordenadas (X, Y, Z):")

    def add_point(self):
        try:
            points = self.coord_entry.get()
            points = points.split(';')  # Permitir múltiplos pontos separados por ponto-e-vírgula
            for point in points:
                coords = list(map(float, point.split(',')))
                while len(coords) < 3:  # Preencher Z como 0 se não fornecido
                    coords.append(0)
                x, y, z = coords
                self.points.append((x, y, z))
                self.coords_listbox.insert(tk.END, f"({x}, {y}, {z})")
            self.coord_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Insira as coordenadas no formato X,Y[,Z] ou X1,Y1,Z1;X2,Y2,Z2.")

    def finish_object(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Erro", "O nome do objeto não pode estar vazio.")
            return

        obj_type = self.obj_type_selector.get()
        if obj_type == "Linha" and len(self.points) != 2:
            messagebox.showerror("Erro", "Uma linha requer exatamente 2 pontos.")
            return
        if obj_type in ["Polilinha", "Polígono"] and len(self.points) < 2:
            messagebox.showerror("Erro", f"Uma {obj_type.lower()} requer pelo menos 2 pontos.")
            return
        if obj_type == "Polígono":
            self.points.append(self.points[0])  # Fecha automaticamente

        # Adicionar o objeto à lista de exibição
        graphic_object = GraphicObject(obj_type, name, self.points)
        self.display_list.append(graphic_object)
        self.update_viewport()
        self.update_listbox()

        messagebox.showinfo("Sucesso", f"Objeto '{name}' adicionado!")
        self.add_window.destroy()
