# main.py

from tkinter import Tk
from graphic_system import GraphicSystem

if __name__ == "__main__":
    root = Tk()
    root.title("Sistema Gráfico")
    app = GraphicSystem(root)
    root.mainloop()
