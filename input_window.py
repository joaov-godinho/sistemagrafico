#input_window
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from graphic_object import GraphicObject


class InputWindow:
    def __init__(self, root, obj_type, display_list, update_viewport, update_listbox, is_line=False, is_polyline=False):
        self.root = root
        self.obj_type = obj_type
        self.is_line = is_line
        self.is_polyline = is_polyline
        self.display_list = display_list
        self.update_viewport = update_viewport
        self.update_listbox = update_listbox
        self.points = []
        self.init_window()

    def init_window(self):
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title(f"Adicionar {self.obj_type}")

        Label(self.input_window, text="Nome do Objeto:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.name_entry = Entry(self.input_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.input_window, text="Coordenadas (X, Y):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.coord_entry = Entry(self.input_window)
        self.coord_entry.grid(row=1, column=1, padx=10, pady=5)

        Button(self.input_window, text="Adicionar Ponto", command=self.add_point).grid(row=2, column=0, columnspan=2, pady=10)

        if self.is_line or self.is_polyline:
            Button(self.input_window, text="Adicionar Linha/Polilinha", command=self.add_line_or_polyline).grid(row=3, column=0, columnspan=2, pady=10)

        Button(self.input_window, text="Finalizar Objeto", command=self.finish_object).grid(row=4, column=0, columnspan=2, pady=10)

    def add_point(self):
        try:
            x, y = map(float, self.coord_entry.get().split(','))
            self.points.append((x, y))
            self.coord_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", f"Ponto ({x}, {y}) adicionado!")
        except ValueError:
            messagebox.showerror("Erro", "Insira as coordenadas no formato X,Y.")

    def add_line_or_polyline(self):
        try:
            x, y = map(float, self.coord_entry.get().split(','))
            self.points.append((x, y))
            self.coord_entry.delete(0, tk.END)

            if self.is_line and len(self.points) == 2:
                messagebox.showinfo("Sucesso", f"Linha adicionada entre os pontos {self.points[0]} e {self.points[1]}")
            elif self.is_polyline:
                messagebox.showinfo("Sucesso", f"Ponto {self.points[-1]} adicionado à polilinha")

        except ValueError:
            messagebox.showerror("Erro", "Insira as coordenadas no formato X,Y.")

    def finish_object(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Erro", "O nome do objeto não pode estar vazio.")
            return

        # Validações para diferentes tipos de objetos
        if self.obj_type == "Polilinha" and len(self.points) < 2:
            messagebox.showerror("Erro", "Uma polilinha precisa de pelo menos 2 pontos.")
            return
        elif self.obj_type == "Polígono" and len(self.points) < 3:
            messagebox.showerror("Erro", "Um polígono precisa de pelo menos 3 pontos.")
            return
        elif self.obj_type == "Polígono":
            self.points.append(self.points[0])  # Fecha automaticamente

        # Cria o objeto gráfico
        graphic_object = GraphicObject(self.obj_type, name, self.points)
        self.display_list.append(graphic_object)
        self.update_viewport()
        self.update_listbox()

        messagebox.showinfo("Sucesso", f"Objeto '{name}' adicionado!")
        self.input_window.destroy()
