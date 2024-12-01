import tkinter as tk
from tkinter import ttk, messagebox
from transformations import apply_translation, apply_rotation, apply_scaling, apply_shear, apply_reflection

class TransformationWindow:
    def __init__(self, root, display_list, selected_indices, update_viewport):
        self.root = root
        self.display_list = display_list
        self.selected_indices = selected_indices
        self.update_viewport = update_viewport
        self.init_window()

    def init_window(self):
        self.transformation_window = tk.Toplevel(self.root)
        self.transformation_window.title("Transformações")

        # Configuração de abas
        tab_control = ttk.Notebook(self.transformation_window)

        # Aba de Translação
        translation_tab = ttk.Frame(tab_control)
        tab_control.add(translation_tab, text="Translação")

        tk.Label(translation_tab, text="Dx:").grid(row=0, column=0, padx=10, pady=5)
        self.dx_entry = tk.Entry(translation_tab)
        self.dx_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(translation_tab, text="Dy:").grid(row=1, column=0, padx=10, pady=5)
        self.dy_entry = tk.Entry(translation_tab)
        self.dy_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(translation_tab, text="Dz:").grid(row=2, column=0, padx=10, pady=5)
        self.dz_entry = tk.Entry(translation_tab)
        self.dz_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(translation_tab, text="Aplicar Translação", command=self.apply_translation).grid(row=3, column=0, columnspan=2, pady=10)

        # Aba de Rotação
        rotation_tab = ttk.Frame(tab_control)
        tab_control.add(rotation_tab, text="Rotação")

        # Ângulo de Rotação
        tk.Label(rotation_tab, text="Ângulo (°):").grid(row=0, column=0, padx=10, pady=5)
        self.angle_entry = tk.Entry(rotation_tab)
        self.angle_entry.grid(row=0, column=1, padx=10, pady=5)

        # Adicione uma lista suspensa para selecionar o eixo
        self.rotation_axis = tk.StringVar(value='z')
        tk.Label(rotation_tab, text="Eixo de Rotação:").grid(row=4, column=0, padx=10, pady=5)
        tk.OptionMenu(rotation_tab, self.rotation_axis, 'x', 'y', 'z').grid(row=4, column=1, padx=10, pady=5)

        # Checkboxes para modos de rotação
        self.rotate_origin_var = tk.BooleanVar(value=False)
        self.rotate_point_var = tk.BooleanVar(value=False)

        self.rotate_origin_checkbox = tk.Checkbutton(
            rotation_tab,
            text="Rotacionar sobre a origem",
            variable=self.rotate_origin_var,
            command=self.toggle_rotation_mode
        )
        self.rotate_origin_checkbox.grid(row=1, column=0, padx=10, pady=5)

        self.rotate_point_checkbox = tk.Checkbutton(
            rotation_tab,
            text="Rotacionar sobre um ponto qualquer",
            variable=self.rotate_point_var,
            command=self.toggle_rotation_mode
        )
        self.rotate_point_checkbox.grid(row=2, column=0, padx=10, pady=5)

        # Campos para ponto de rotação
        tk.Label(rotation_tab, text="Centro de Rotação (Cx, Cy):").grid(row=3, column=0, padx=10, pady=5)
        self.cx_cy_entry = tk.Entry(rotation_tab, state="disabled")  # Inicialmente desabilitado
        self.cx_cy_entry.grid(row=3, column=1, padx=10, pady=5)

        # Botão de Aplicar Rotação
        tk.Button(rotation_tab, text="Aplicar Rotação", command=self.apply_rotation).grid(row=6, column=0, columnspan=2, pady=10)

        # Aba de Escalonamento
        scaling_tab = ttk.Frame(tab_control)
        tab_control.add(scaling_tab, text="Escalonamento")

        # Fator de Escala
        tk.Label(scaling_tab, text="Fator de Escala:").grid(row=0, column=0, padx=10, pady=5)
        self.scale_entry = tk.Entry(scaling_tab)
        self.scale_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(scaling_tab, text="Centro de Escalonamento (Cx, Cy, Cz):").grid(row=3, column=0, padx=10, pady=5)
        self.scale_cx_cy_cz_entry = tk.Entry(scaling_tab, state="disabled")
        self.scale_cx_cy_cz_entry.grid(row=3, column=1, padx=10, pady=5)

        # Checkboxes para modos de escalonamento
        self.scale_origin_var = tk.BooleanVar(value=False)
        self.scale_point_var = tk.BooleanVar(value=False)

        self.scale_origin_checkbox = tk.Checkbutton(
            scaling_tab,
            text="Escalonar em relação à origem",
            variable=self.scale_origin_var,
            command=self.toggle_scaling_mode
        )
        self.scale_origin_checkbox.grid(row=1, column=0, padx=10, pady=5)

        self.scale_point_checkbox = tk.Checkbutton(
            scaling_tab,
            text="Escalonar em relação a um ponto qualquer",
            variable=self.scale_point_var,
            command=self.toggle_scaling_mode
        )
        self.scale_point_checkbox.grid(row=2, column=0, padx=10, pady=5)

        # Botão de Aplicar Escalonamento
        tk.Button(scaling_tab, text="Aplicar Escalonamento", command=self.apply_scaling).grid(row=4, column=0, columnspan=2, pady=10)

        # Aba de Reflexão
        reflection_tab = ttk.Frame(tab_control)
        tab_control.add(reflection_tab, text="Reflexão")

        # Checkboxes para os eixos de reflexão
        self.reflect_x_var = tk.BooleanVar(value=False)
        self.reflect_y_var = tk.BooleanVar(value=False)

        tk.Checkbutton(reflection_tab, text="Refletir em torno do eixo X", variable=self.reflect_x_var).grid(row=0, column=0, padx=10, pady=5)
        tk.Checkbutton(reflection_tab, text="Refletir em torno do eixo Y", variable=self.reflect_y_var).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(reflection_tab, text="Aplicar Reflexão", command=self.apply_reflection).grid(row=2, column=0, columnspan=2, pady=10)

        # Aba de Cisalhamento
        shear_tab = ttk.Frame(tab_control)
        tab_control.add(shear_tab, text="Cisalhamento")

        # Entradas para os valores de cisalhamento
        tk.Label(shear_tab, text="Shx:").grid(row=0, column=0, padx=10, pady=5)
        self.shx_entry = tk.Entry(shear_tab)
        self.shx_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(shear_tab, text="Shy:").grid(row=1, column=0, padx=10, pady=5)
        self.shy_entry = tk.Entry(shear_tab)
        self.shy_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(shear_tab, text="Aplicar Cisalhamento", command=self.apply_shear).grid(row=2, column=0, columnspan=2, pady=10)

        tab_control.pack(expand=1, fill="both")

    def apply_translation(self):
        try:
            dx = float(self.dx_entry.get())
            dy = float(self.dy_entry.get())
            dz = float(self.dz_entry.get()) if self.dz_entry.get() else 0
            for idx in self.selected_indices:
                apply_translation(self.display_list[idx], dx, dy, dz)
            self.update_viewport()
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos para dx, dy e dz.")

    def toggle_rotation_mode(self):
        if self.rotate_origin_var.get():
            self.cx_cy_entry.configure(state="disabled")  # Desabilita o campo de ponto
            self.rotate_point_var.set(False)  # Desmarca a outra checkbox
        elif self.rotate_point_var.get():
            self.cx_cy_entry.configure(state="normal")  # Habilita o campo de ponto
            self.rotate_origin_var.set(False)  # Desmarca a outra checkbox

    def apply_rotation(self):
        try:
            angle = float(self.angle_entry.get())  # Obtém o ângulo de rotação
            axis = self.rotation_axis.get()  # Obtém o eixo de rotação selecionado

            # Verifica qual modo de rotação foi selecionado
            if self.rotate_origin_var.get():  # Rotacionar sobre a origem
                cx, cy, cz = 0, 0, 0  # Define a origem como centro de rotação
            elif self.rotate_point_var.get():  # Rotacionar sobre um ponto qualquer
                cx, cy, cz = map(float, self.cx_cy_entry.get().split(','))  # Obtém o ponto de rotação
            else:
                messagebox.showerror("Erro", "Selecione um modo de rotação.")
                return

            # Aplica a rotação para os objetos selecionados
            for idx in self.selected_indices:
                apply_rotation(self.display_list[idx], angle, axis, cx, cy, cz)

            # Atualiza a viewport após a rotação
            self.update_viewport()

        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos para o ângulo, o eixo e o ponto de rotação, se necessário.")


        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos para o ângulo e o ponto de rotação, se necessário.")

    def toggle_scaling_mode(self):
        if self.scale_origin_var.get():
            self.scale_cx_cy_cz_entry.configure(state="disabled")  # Desabilita o campo de ponto
            self.scale_point_var.set(False)  # Desmarca a outra checkbox
        elif self.scale_point_var.get():
            self.scale_cx_cy_cz_entry.configure(state="normal")  # Habilita o campo de ponto
            self.scale_origin_var.set(False)  # Desmarca a outra checkbox

    def apply_scaling(self):
        try:
            # Obtém o fator de escala
            scale_factor = float(self.scale_entry.get())

            # Verifica qual modo de escalonamento foi selecionado
            if self.scale_origin_var.get():  # Escalonar em relação à origem
                cx, cy, cz = 0, 0, 0  # Define a origem como centro de escalonamento
            elif self.scale_point_var.get():  # Escalonar em relação a um ponto qualquer
                cx, cy, cz = map(float, self.scale_cx_cy_cz_entry.get().split(','))  # Obtém o ponto de escalonamento
            else:
                messagebox.showerror("Erro", "Selecione um modo de escalonamento.")
                return

            # Aplica o escalonamento para os objetos selecionados
            for idx in self.selected_indices:
                obj = self.display_list[idx]
                apply_scaling(obj, scale_factor, cx, cy, cz)

            # Atualiza a viewport após o escalonamento
            self.update_viewport()

        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos para o fator de escala e o ponto de escalonamento.")


    def apply_reflection(self):
        try:
            reflect_x = self.reflect_x_var.get()
            reflect_y = self.reflect_y_var.get()
            
            # Aplica a reflexão aos objetos selecionados
            for idx in self.selected_indices:
                obj = self.display_list[idx]
                apply_reflection(obj, reflect_x=reflect_x, reflect_y=reflect_y)
            
            # Atualiza a viewport
            self.update_viewport()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar reflexão: {e}")

    def apply_shear(self):
        try:
            shx = float(self.shx_entry.get()) if self.shx_entry.get() else 0
            shy = float(self.shy_entry.get()) if self.shy_entry.get() else 0
            
            # Aplica o cisalhamento aos objetos selecionados
            for idx in self.selected_indices:
                obj = self.display_list[idx]
                apply_shear(obj, shx=shx, shy=shy)
            
            # Atualiza a viewport
            self.update_viewport()
        except ValueError:
            messagebox.showerror("Erro", "Insira valores numéricos válidos para Shx e Shy.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar cisalhamento: {e}")


