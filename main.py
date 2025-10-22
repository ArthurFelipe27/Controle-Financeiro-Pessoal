import ttkbootstrap as ttk
from telas import App
from database import criar_tabelas
import matplotlib.pyplot as plt

# Arquivo principal que inicia a aplicação.

def on_closing(root):
    """
    Função para garantir que o programa seja encerrado corretamente.
    Fecha todas as janelas de gráficos do Matplotlib antes de fechar a janela principal.
    """
    plt.close('all')  # Fecha todas as figuras do matplotlib
    root.destroy()    # Destrói a janela do tkinter

if __name__ == "__main__":
    # Garante que as tabelas sejam criadas na primeira execução
    criar_tabelas()
    
    # Cria a janela principal aplicando o tema "litera"
    root = ttk.Window(themename="litera")
    
    app = App(root)
    
    # --- CORREÇÃO: Adiciona o protocolo para o botão de fechar ---
    # Intercepta o clique no botão 'X' da janela e chama a função on_closing
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    root.mainloop()

