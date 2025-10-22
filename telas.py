import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
import datetime

# Importa as funções de lógica de negócios dos outros arquivos
from database import resetar_banco
import categoria_crud as cat_crud
import transacao_crud as tran_crud
import relatorio as rel

# --- CLASSE PRINCIPAL DA APLICAÇÃO (UI) ---

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Controle Financeiro Pessoal")
        self.master.geometry("800x600")
        self.master.minsize(700, 500) # Define um tamanho mínimo para a janela
        self.frame_atual = None
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        self.mostrar_menu_principal()

    def _limpar_frame(self):
        """Destrói o frame atual e cria um novo para a próxima tela."""
        if self.frame_atual:
            self.frame_atual.destroy()
        self.frame_atual = ttk.Frame(self.master, padding=(20, 10))
        self.frame_atual.pack(fill=BOTH, expand=YES)

    # --- TELA PRINCIPAL ---
    def mostrar_menu_principal(self):
        self._limpar_frame()
        ttk.Label(self.frame_atual, text="Controle Financeiro", font=("Helvetica", 24, "bold"), bootstyle=PRIMARY).pack(pady=20)
        
        self.saldo_label = ttk.Label(self.frame_atual, text="", font=("Helvetica", 18))
        self.saldo_label.pack(pady=20)
        self.atualizar_saldo()

        btn_frame = ttk.Frame(self.frame_atual)
        btn_frame.pack(pady=20)
        
        button_style = {'width': 30, 'bootstyle': (PRIMARY, OUTLINE)}
        ttk.Button(btn_frame, text="Gerenciar Transações", command=self.mostrar_transacoes, **button_style).pack(pady=8, ipady=5)
        ttk.Button(btn_frame, text="Gerenciar Categorias", command=self.mostrar_categorias, **button_style).pack(pady=8, ipady=5)
        ttk.Button(btn_frame, text="Ver Relatórios", command=self.mostrar_relatorio, **button_style).pack(pady=8, ipady=5)
        ttk.Button(btn_frame, text="Resetar Banco de Dados", command=self.resetar_banco_dados, bootstyle=DANGER).pack(pady=25, ipady=5)

    def atualizar_saldo(self):
        receitas, despesas = rel.get_dados_relatorio("0001-01-01", "9999-12-31")
        saldo = receitas - despesas
        cor = SUCCESS if saldo >= 0 else DANGER
        # --- CORREÇÃO: Verifica se o widget existe antes de tentar configurá-lo ---
        # Isso previne o erro quando esta função é chamada de outra tela.
        if hasattr(self, 'saldo_label') and self.saldo_label.winfo_exists():
            self.saldo_label.config(text=f"Saldo Total: R$ {saldo:,.2f}", bootstyle=cor)

    def resetar_banco_dados(self):
        if messagebox.askyesno("Resetar Banco", "Tem certeza que deseja apagar TUDO? Esta ação não pode ser desfeita.", icon='warning'):
            resetar_banco()
            self.atualizar_saldo()
            messagebox.showinfo("Sucesso", "Banco de dados resetado com sucesso!")

    # --- TELA DE CATEGORIAS ---
    def mostrar_categorias(self):
        self._limpar_frame()
        header_frame = ttk.Frame(self.frame_atual)
        header_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(header_frame, text="Gerenciar Categorias", font=("Helvetica", 16, "bold")).pack(side=LEFT)
        
        tree_frame = ttk.Frame(self.frame_atual)
        tree_frame.pack(fill=BOTH, expand=YES)
        
        cols = ('ID', 'Nome')
        self.tree_cat = ttk.Treeview(tree_frame, columns=cols, show='headings', bootstyle=PRIMARY)
        self.tree_cat.heading('ID', text='ID')
        self.tree_cat.heading('Nome', text='Nome da Categoria')
        self.tree_cat.column('ID', width=80, anchor=CENTER)
        self.tree_cat.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree_cat.yview, bootstyle="round")
        self.tree_cat.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.carregar_dados_categorias()

        btn_frame = ttk.Frame(self.frame_atual)
        btn_frame.pack(pady=15, fill=X, side=BOTTOM)
        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar_categoria_ui, bootstyle=SUCCESS).pack(side=LEFT, expand=YES, padx=5, ipady=4)
        ttk.Button(btn_frame, text="Editar", command=self.editar_categoria_ui, bootstyle=INFO).pack(side=LEFT, expand=YES, padx=5, ipady=4)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_categoria_ui, bootstyle=DANGER).pack(side=LEFT, expand=YES, padx=5, ipady=4)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=self.mostrar_menu_principal, bootstyle=(SECONDARY, OUTLINE)).pack(side=LEFT, expand=YES, padx=5, ipady=4)

    def carregar_dados_categorias(self):
        for i in self.tree_cat.get_children():
            self.tree_cat.delete(i)
        for cat in cat_crud.listar_categorias():
            self.tree_cat.insert("", END, values=cat)
            
    def adicionar_categoria_ui(self):
        nome = simpledialog.askstring("Nova Categoria", "Digite o nome da categoria:")
        if nome:
            try:
                cat_crud.adicionar_categoria(nome)
                self.carregar_dados_categorias()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e))

    def _get_selected_item_from_tree(self, tree):
        selecao = tree.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Por favor, selecione um item na tabela.")
            return None
        return tree.item(selecao[0])['values']

    def editar_categoria_ui(self):
        item = self._get_selected_item_from_tree(self.tree_cat)
        if not item: return
        id_cat, nome_atual = item
        novo_nome = simpledialog.askstring("Editar Categoria", "Novo nome:", initialvalue=nome_atual)
        if novo_nome:
            try:
                cat_crud.atualizar_categoria(id_cat, novo_nome)
                self.carregar_dados_categorias()
            except ValueError as e:
                messagebox.showerror("Erro de Validação", str(e))
            
    def excluir_categoria_ui(self):
        item = self._get_selected_item_from_tree(self.tree_cat)
        if not item: return
        id_cat, nome = item
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir a categoria '{nome}'?\nIsso desvinculará as transações associadas.", icon='warning'):
            cat_crud.excluir_categoria(id_cat)
            self.carregar_dados_categorias()
            self.carregar_dados_transacoes() if hasattr(self, 'tree_tran') else None


    # --- TELA DE TRANSAÇÕES ---
    def mostrar_transacoes(self):
        self._limpar_frame()
        ttk.Label(self.frame_atual, text="Gerenciar Transações", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        
        tree_frame = ttk.Frame(self.frame_atual)
        tree_frame.pack(fill=BOTH, expand=YES)

        cols = ('ID', 'Data', 'Valor', 'Tipo', 'Categoria')
        self.tree_tran = ttk.Treeview(tree_frame, columns=cols, show='headings', bootstyle=PRIMARY)
        for col in cols: self.tree_tran.heading(col, text=col)
        
        self.tree_tran.column('ID', width=50, anchor=CENTER)
        self.tree_tran.column('Data', width=100, anchor=CENTER)
        self.tree_tran.column('Valor', width=120, anchor='e')
        self.tree_tran.column('Tipo', width=100, anchor=CENTER)
        self.tree_tran.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree_tran.yview, bootstyle="round")
        self.tree_tran.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.carregar_dados_transacoes()

        btn_frame = ttk.Frame(self.frame_atual)
        btn_frame.pack(pady=15, fill=X, side=BOTTOM)
        ttk.Button(btn_frame, text="Adicionar", command=lambda: self.abrir_formulario_transacao(), bootstyle=SUCCESS).pack(side=LEFT, expand=YES, padx=5, ipady=4)
        ttk.Button(btn_frame, text="Editar", command=self.editar_transacao_ui, bootstyle=INFO).pack(side=LEFT, expand=YES, padx=5, ipady=4)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_transacao_ui, bootstyle=DANGER).pack(side=LEFT, expand=YES, padx=5, ipady=4)
        ttk.Button(btn_frame, text="Voltar ao Menu", command=self.mostrar_menu_principal, bootstyle=(SECONDARY, OUTLINE)).pack(side=LEFT, expand=YES, padx=5, ipady=4)

    def carregar_dados_transacoes(self):
        for i in self.tree_tran.get_children(): self.tree_tran.delete(i)
        for t in tran_crud.listar_transacoes():
            id_, data, valor, tipo, categoria = t
            valor_formatado = f"R$ {valor:,.2f}"
            self.tree_tran.insert("", END, values=(id_, data, valor_formatado, tipo, categoria or "N/A"), tags=(tipo,))
        self.tree_tran.tag_configure('Receita', foreground='green')
        self.tree_tran.tag_configure('Despesa', foreground='red')

    def editar_transacao_ui(self):
        item = self._get_selected_item_from_tree(self.tree_tran)
        if not item: return
        self.abrir_formulario_transacao(item[0])

    def excluir_transacao_ui(self):
        item = self._get_selected_item_from_tree(self.tree_tran)
        if not item: return
        id_tran = item[0]
        if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir a transação ID {id_tran}?", icon='warning'):
            tran_crud.excluir_transacao(id_tran)
            self.carregar_dados_transacoes()
            self.atualizar_saldo()

    def abrir_formulario_transacao(self, id_transacao=None):
        on_save_callback = lambda: [self.carregar_dados_transacoes(), self.atualizar_saldo()]
        FormularioTransacao(self.master, id_transacao, on_save=on_save_callback)


    # --- TELA DE RELATÓRIOS ---
    def mostrar_relatorio(self):
        self._limpar_frame()
        ttk.Label(self.frame_atual, text="Relatório Financeiro", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        filtros_frame = ttk.Frame(self.frame_atual)
        filtros_frame.pack(pady=10)
        
        ttk.Label(filtros_frame, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5)
        self.data_inicial_rel = ttk.DateEntry(filtros_frame, dateformat='%Y-%m-%d', startdate=datetime.date.today().replace(day=1))
        self.data_inicial_rel.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filtros_frame, text="Data Final:").grid(row=1, column=0, padx=5, pady=5)
        self.data_final_rel = ttk.DateEntry(filtros_frame, dateformat='%Y-%m-%d', startdate=datetime.date.today())
        self.data_final_rel.grid(row=1, column=1, padx=5, pady=5)
        
        resultado_frame = ttk.Labelframe(self.frame_atual, text="Resumo do Período", padding=20)
        resultado_frame.pack(pady=20, padx=20, fill='x')
        
        self.saldo_label_rel = ttk.Label(resultado_frame, text="Selecione o período e clique em gerar.", font=("Arial", 11), justify=LEFT)
        self.saldo_label_rel.pack()

        btn_frame_rel = ttk.Frame(self.frame_atual)
        btn_frame_rel.pack(pady=10)
        ttk.Button(btn_frame_rel, text="Gerar Relatório e Gráfico", command=self.gerar_relatorio_ui, bootstyle=SUCCESS).pack(side=LEFT, padx=10, ipady=5)
        ttk.Button(btn_frame_rel, text="Voltar ao Menu", command=self.mostrar_menu_principal, bootstyle=(SECONDARY, OUTLINE)).pack(side=LEFT, padx=10, ipady=5)

    def gerar_relatorio_ui(self):
        ini = self.data_inicial_rel.entry.get()
        fim = self.data_final_rel.entry.get()
        
        receitas, despesas = rel.get_dados_relatorio(ini, fim)
        saldo = receitas - despesas
        cor = SUCCESS if saldo >= 0 else DANGER
        
        texto = f"Receitas: R$ {receitas:,.2f}\nDespesas: R$ {despesas:,.2f}\n\nSaldo no Período: R$ {saldo:,.2f}"
        self.saldo_label_rel.config(text=texto, bootstyle=cor)

        categorias = rel.get_despesas_por_categoria(ini, fim)
        if not rel.gerar_grafico_despesas(categorias):
            messagebox.showinfo("Sem Dados", "Não há despesas no período selecionado para gerar um gráfico.")

# --- CLASSE PARA O FORMULÁRIO DE TRANSAÇÃO (Janela Toplevel) ---
class FormularioTransacao(ttk.Toplevel):
    def __init__(self, parent, id_transacao=None, on_save=None):
        super().__init__(parent)
        self.id_transacao = id_transacao
        self.on_save = on_save

        self.title("Editar Transação" if id_transacao else "Nova Transação")
        self.geometry("400x420")
        self.transient(parent)
        self.grab_set()

        container = ttk.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Dados iniciais para o formulário
        self.dados_iniciais = {}
        if id_transacao:
            self.dados_iniciais = tran_crud.buscar_transacao_por_id(self.id_transacao)
            if not self.dados_iniciais:
                messagebox.showerror("Erro", "Transação não encontrada.", parent=self)
                self.destroy()
                return
        
        # Widgets
        ttk.Label(container, text="Data:").pack(pady=(10, 2))
        data_inicial = self.dados_iniciais.get('data', datetime.date.today())
        self.entry_data = ttk.DateEntry(container, dateformat='%Y-%m-%d', startdate=data_inicial)
        self.entry_data.pack()

        ttk.Label(container, text="Valor (R$):").pack(pady=(10, 2))
        self.entry_valor = ttk.Entry(container)
        self.entry_valor.pack()

        ttk.Label(container, text="Tipo:").pack(pady=(10, 2))
        self.tipo_var = ttk.StringVar()
        self.combo_tipo = ttk.Combobox(container, textvariable=self.tipo_var, state="readonly", values=("Receita", "Despesa"))
        self.combo_tipo.pack()

        ttk.Label(container, text="Categoria:").pack(pady=(10, 2))
        self.categoria_var = ttk.StringVar()
        self.categorias = {nome: id_ for id_, nome in cat_crud.listar_categorias()}
        self.combo_categoria = ttk.Combobox(container, textvariable=self.categoria_var, state="readonly", values=[""] + list(self.categorias.keys()))
        self.combo_categoria.pack()

        ttk.Button(container, text="Salvar", command=self.salvar, bootstyle=SUCCESS).pack(pady=20, ipady=5, fill=X)
        
        if id_transacao:
            self.carregar_dados()

    def carregar_dados(self):
        valor = self.dados_iniciais.get('valor', 0.0)
        tipo = self.dados_iniciais.get('tipo', '')
        cat_id = self.dados_iniciais.get('cat_id')
        
        self.entry_valor.insert(0, f"{valor:.2f}")
        self.tipo_var.set(tipo)
        if cat_id:
            for nome, id_ in self.categorias.items():
                if id_ == cat_id:
                    self.categoria_var.set(nome)
                    break

    def salvar(self):
        try:
            data = self.entry_data.entry.get()
            valor_str = self.entry_valor.get().replace(",", ".")
            tipo = self.tipo_var.get()
            
            if not all([data, valor_str, tipo]):
                raise ValueError("Preencha os campos Data, Valor e Tipo.")
            
            try:
                valor = float(valor_str)
            except ValueError:
                raise ValueError("O valor inserido não é um número válido.")

            cat_selecionada = self.categoria_var.get()
            cat_id = self.categorias.get(cat_selecionada)

            if self.id_transacao:
                tran_crud.atualizar_transacao(self.id_transacao, data, valor, tipo, cat_id)
            else:
                tran_crud.adicionar_transacao(data, valor, tipo, cat_id)
            
            if self.on_save:
                self.on_save()
            
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=self)

