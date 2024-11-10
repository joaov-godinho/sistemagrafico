# input_window.py

import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
from graphic_object import GraphicObject

class InputWindow:
    def __init__(self, root, obj_type, is_line, is_polyline, display_list, update_viewport, update_listbox):
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
        input_window = tk.Toplevel(self.root)
        input_window.title(f"Adicionar {self.obj_type}")

        Label(input_window, text="Nome do objeto:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.name_entry = Entry(input_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(input_window, text="Coordenada X1:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.x1_entry = Entry(input_window)
        self.x1_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(input_window, text="Coordenada Y1:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.y1_entry = Entry(input_window)
        self.y1_entry.grid(row=2, column=1, padx=10, pady=5)

        if self.is_line:
            Label(input_window, text="Coordenada X2:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
            self.x2_entry = Entry(input_window)
            self.x2_entry.grid(row=3, column=1, padx=10, pady=5)

            Label(input_window, text="Coordenada Y2:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
            self.y2_entry = Entry(input_window)
            self.y2_entry.grid(row=4, column=1, padx=10, pady=5)

            Button(input_window, text="Adicionar Linha", width=20, command=self.add_point).grid(row=5, column=0, columnspan=2, pady=10)
        else:
            Button(input_window, text="Adicionar Ponto", width=20, command=self.add_point).grid(row=3, column=0, columnspan=2, pady=10)

        Button(input_window, text="Finalizar", width=20, command=self.finish).grid(row=6, column=0, columnspan=2, pady=10)

    def add_point(self):
        try:
            if self.is_line:
                x1 = float(self.x1_entry.get())
                y1 = float(self.y1_entry.get())
                x2 = float(self.x2_entry.get())
                y2 = float(self.y2_entry.get())
                self.points.append((x1, y1))
                self.points.append((x2, y2))
            else:
                x = float(self.x1_entry.get())
                y = float(self.y1_entry.get())
                self.points.append((x, y))

            self.x1_entry.delete(0, tk.END)
            self.y1_entry.delete(0, tk.END)
            if self.is_line:
                self.x2_entry.delete(0, tk.END)
                self.y2_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Coordenadas inválidas")

    def finish(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Erro", "O nome do objeto não pode estar vazio.")
            return

        if not self.is_line and self.obj_type == "Polilinha" and len(self.points) < 2:
            messagebox.showerror("Erro", "Polilinha precisa de pelo menos 2 pontos")
            return
        elif not self.is_line and self.obj_type == "Polígono" and len(self.points) < 3:
            messagebox.showerror("Erro", "Polígono precisa de pelo menos 3 pontos")
            return
        else:
            if self.obj_type == "Polígono":
                self.points.append(self.points[0])  # Fecha o polígono
            graphic_object = GraphicObject(self.obj_type, name, self.points)
            self.display_list.append(graphic_object)
            self.update_viewport()
            self.update_listbox()