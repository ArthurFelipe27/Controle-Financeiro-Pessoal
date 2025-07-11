import tkinter as tk
from telas import App
from database import criar_tabelas

# Cria o banco e as tabelas se ainda não existirem
# Inicia a interface gráfica

if __name__ == "__main__":
    criar_tabelas()
    root = tk.Tk()
    app = App(root)
    root.mainloop()