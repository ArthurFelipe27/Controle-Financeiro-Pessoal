import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from database import conectar, resetar_banco
import datetime
import matplotlib.pyplot as plt

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Controle Financeiro")
        self.master.geometry("650x550")
        self.frame_atual = None

        self.mostrar_menu_principal()

    def limpar_frame(self):
        """Remove o frame atual"""
        if self.frame_atual:
            self.frame_atual.destroy()

    def mostrar_menu_principal(self):
        """Tela inicial com saldo e botões"""
        self.limpar_frame()
        self.frame_atual = tk.Frame(self.master)
        self.frame_atual.pack(fill="both", expand=True)

        tk.Label(self.frame_atual, text="Controle Financeiro", font=("Arial", 20)).pack(pady=20)

        # Saldo
        self.saldo_label = tk.Label(self.frame_atual, text="", font=("Arial", 16))
        self.saldo_label.pack(pady=10)
        self.atualizar_saldo()

        # Botões principais
        tk.Button(self.frame_atual, text="Gerenciar Categorias", width=30, command=self.mostrar_categorias).pack(pady=5)
        tk.Button(self.frame_atual, text="Gerenciar Transações", width=30, command=self.mostrar_transacoes).pack(pady=5)
        tk.Button(self.frame_atual, text="Ver Relatório", width=30, command=self.mostrar_relatorio).pack(pady=5)
        tk.Button(self.frame_atual, text="Resetar Banco de Dados", width=30, bg="red", fg="white", command=self.resetar_banco_dados).pack(pady=20)

    def atualizar_saldo(self):
        """Atualiza o saldo na tela"""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM transacoes WHERE tipo = 'Receita'")
        receitas = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM transacoes WHERE tipo = 'Despesa'")
        despesas = cursor.fetchone()[0]
        saldo = receitas - despesas
        cor = "green" if saldo >= 0 else "red"
        self.saldo_label.config(text=f"Saldo Total: R$ {saldo:.2f}", fg=cor)
        conn.close()

    def resetar_banco_dados(self):
        """Reseta o banco"""
        if messagebox.askyesno("Resetar Banco", "Tem certeza que deseja apagar tudo?"):
            resetar_banco()
            self.atualizar_saldo()
            messagebox.showinfo("Sucesso", "Banco de dados resetado com sucesso!")

    def mostrar_categorias(self):
        """Tela de categorias"""
        self.limpar_frame()
        self.frame_atual = tk.Frame(self.master)
        self.frame_atual.pack(fill="both", expand=True)

        tk.Label(self.frame_atual, text="Gerenciar Categorias", font=("Arial", 16)).pack(pady=10)

        lista = tk.Listbox(self.frame_atual, width=50)
        lista.pack(pady=10)

        def carregar_categorias():
            lista.delete(0, tk.END)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
            for id_, nome in cursor.fetchall():
                lista.insert(tk.END, f"{id_} - {nome}")
            conn.close()

        carregar_categorias()

        def adicionar_categoria():
            nome = simpledialog.askstring("Nova Categoria", "Digite o nome da categoria:")
            if nome:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome.strip(),))
                conn.commit()
                conn.close()
                carregar_categorias()

        def editar_categoria():
            selecao = lista.curselection()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione uma categoria.")
                return
            item = lista.get(selecao[0])
            id_categoria, nome_atual = item.split(" - ", 1)
            novo_nome = simpledialog.askstring("Editar Categoria", "Novo nome:", initialvalue=nome_atual)
            if novo_nome:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("UPDATE categorias SET nome=? WHERE id=?", (novo_nome.strip(), id_categoria))
                conn.commit()
                conn.close()
                carregar_categorias()

        def excluir_categoria():
            selecao = lista.curselection()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione uma categoria.")
                return
            item = lista.get(selecao[0])
            id_categoria = item.split(" - ")[0]
            if messagebox.askyesno("Excluir", "Excluir esta categoria?"):
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM categorias WHERE id=?", (id_categoria,))
                conn.commit()
                conn.close()
                carregar_categorias()

        btn_frame = tk.Frame(self.frame_atual)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Adicionar", command=adicionar_categoria).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", command=editar_categoria).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Excluir", command=excluir_categoria).grid(row=0, column=2, padx=5)

        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_principal).pack(pady=10)

    def mostrar_transacoes(self):
        """Tela de transações"""
        self.limpar_frame()
        self.frame_atual = tk.Frame(self.master)
        self.frame_atual.pack(fill="both", expand=True)

        tk.Label(self.frame_atual, text="Gerenciar Transações", font=("Arial", 16)).pack(pady=10)

        lista = tk.Listbox(self.frame_atual, width=80)
        lista.pack(pady=10)

        def carregar_transacoes():
            lista.delete(0, tk.END)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, t.data, t.valor, t.tipo, c.nome
                FROM transacoes t
                LEFT JOIN categorias c ON t.categoria_id = c.id
                ORDER BY t.data DESC
            """)
            for transacao in cursor.fetchall():
                id_, data, valor, tipo, categoria = transacao
                lista.insert(
                    tk.END,
                    f"{id_} - {data} | R$ {valor:.2f} | {tipo} | Categoria: {categoria or 'N/A'}"
                )
            conn.close()

        carregar_transacoes()

        def abrir_formulario(id_transacao=None):
            form = tk.Toplevel(self.master)
            form.title("Nova Transação" if id_transacao is None else "Editar Transação")
            form.geometry("400x400")

            tk.Label(form, text="Data:").pack(pady=5)
            entry_data = DateEntry(form, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
            entry_data.set_date(datetime.date.today())
            entry_data.pack()

            tk.Label(form, text="Valor (R$):").pack(pady=5)
            entry_valor = tk.Entry(form)
            entry_valor.pack()

            tk.Label(form, text="Tipo:").pack(pady=5)
            tipo_var = tk.StringVar()
            combo_tipo = ttk.Combobox(form, textvariable=tipo_var, state="readonly")
            combo_tipo['values'] = ("Receita", "Despesa")
            combo_tipo.pack()

            tk.Label(form, text="Categoria:").pack(pady=5)
            categoria_var = tk.StringVar()
            combo_categoria = ttk.Combobox(form, textvariable=categoria_var, state="readonly")
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
            categorias = [f"{id_} - {nome}" for id_, nome in cursor.fetchall()]
            combo_categoria['values'] = categorias
            conn.close()
            combo_categoria.pack()

            if id_transacao:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT data, valor, tipo, categoria_id FROM transacoes WHERE id=?", (id_transacao,))
                data, valor, tipo, categoria_id = cursor.fetchone()
                entry_data.set_date(data)
                entry_valor.insert(0, f"{valor:.2f}")
                tipo_var.set(tipo)
                if categoria_id:
                    for item in categorias:
                        if item.startswith(f"{categoria_id} -"):
                            categoria_var.set(item)
                conn.close()

            def salvar():
                data = entry_data.get()
                valor = entry_valor.get()
                tipo = tipo_var.get()
                categoria = categoria_var.get()

                if not data or not valor or not tipo:
                    messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
                    return
                try:
                    valor_float = float(valor)
                except ValueError:
                    messagebox.showerror("Erro", "O valor deve ser numérico.")
                    return

                categoria_id = None
                if categoria:
                    categoria_id = categoria.split(" - ")[0]

                conn = conectar()
                cursor = conn.cursor()
                if id_transacao:
                    cursor.execute("""
                        UPDATE transacoes SET data=?, valor=?, tipo=?, categoria_id=? WHERE id=?
                    """, (data, valor_float, tipo, categoria_id, id_transacao))
                else:
                    cursor.execute("""
                        INSERT INTO transacoes (data, valor, tipo, categoria_id)
                        VALUES (?, ?, ?, ?)
                    """, (data, valor_float, tipo, categoria_id))
                conn.commit()
                conn.close()
                carregar_transacoes()
                self.atualizar_saldo()
                form.destroy()

            tk.Button(form, text="Salvar", command=salvar).pack(pady=20)

        def adicionar_transacao():
            abrir_formulario()

        def editar_transacao():
            selecao = lista.curselection()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione uma transação.")
                return
            item = lista.get(selecao[0])
            id_transacao = item.split(" - ")[0]
            abrir_formulario(id_transacao)

        def excluir_transacao():
            selecao = lista.curselection()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione uma transação.")
                return
            item = lista.get(selecao[0])
            id_transacao = item.split(" - ")[0]
            if messagebox.askyesno("Excluir", "Excluir esta transação?"):
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transacoes WHERE id=?", (id_transacao,))
                conn.commit()
                conn.close()
                carregar_transacoes()
                self.atualizar_saldo()

        btn_frame = tk.Frame(self.frame_atual)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Adicionar", command=adicionar_transacao).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar", command=editar_transacao).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Excluir", command=excluir_transacao).grid(row=0, column=2, padx=5)

        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_principal).pack(pady=10)

    def mostrar_relatorio(self):
        """Tela de relatório"""
        self.limpar_frame()
        self.frame_atual = tk.Frame(self.master)
        self.frame_atual.pack(fill="both", expand=True)

        tk.Label(self.frame_atual, text="Relatório Financeiro", font=("Arial", 16)).pack(pady=10)

        filtros_frame = tk.Frame(self.frame_atual)
        filtros_frame.pack(pady=10)

        tk.Label(filtros_frame, text="Data Inicial:").grid(row=0, column=0, padx=5)
        data_inicial = DateEntry(filtros_frame, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
        data_inicial.set_date(datetime.date.today().replace(day=1))
        data_inicial.grid(row=0, column=1, padx=5)

        tk.Label(filtros_frame, text="Data Final:").grid(row=1, column=0, padx=5)
        data_final = DateEntry(filtros_frame, width=12, background="darkblue", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
        data_final.set_date(datetime.date.today())
        data_final.grid(row=1, column=1, padx=5)

        saldo_label = tk.Label(self.frame_atual, text="", font=("Arial", 12))
        saldo_label.pack(pady=10)

        def gerar_relatorio():
            ini = data_inicial.get()
            fim = data_final.get()

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tipo, COALESCE(SUM(valor), 0) FROM transacoes
                WHERE data BETWEEN ? AND ?
                GROUP BY tipo
            """, (ini, fim))
            dados = dict(cursor.fetchall())
            receitas = dados.get('Receita', 0)
            despesas = dados.get('Despesa', 0)
            saldo = receitas - despesas

            cor = "green" if saldo >= 0 else "red"
            saldo_label.config(
                text=f"Receitas: R$ {receitas:.2f} | Despesas: R$ {despesas:.2f}\nSaldo: R$ {saldo:.2f}", fg=cor
            )

            cursor.execute("""
                SELECT c.nome, SUM(t.valor) FROM transacoes t
                JOIN categorias c ON t.categoria_id = c.id
                WHERE t.tipo='Despesa' AND t.data BETWEEN ? AND ?
                GROUP BY c.nome
                ORDER BY SUM(t.valor) DESC
            """, (ini, fim))
            categorias = cursor.fetchall()
            conn.close()

            if categorias:
                nomes, valores = zip(*categorias)
                if len(nomes) <= 6:
                    plt.figure(figsize=(6, 4))
                    plt.title("Despesas por Categoria (Pizza)")
                    plt.pie(valores, labels=nomes, autopct="%1.1f%%", startangle=90)
                    plt.axis("equal")
                else:
                    plt.figure(figsize=(8, 5))
                    plt.title("Despesas por Categoria (Barras)")
                    plt.barh(nomes, valores, color="skyblue")
                    plt.xlabel("Valor gasto (R$)")
                    plt.gca().invert_yaxis()

                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("Sem dados", "Não há despesas para o período selecionado.")

        tk.Button(self.frame_atual, text="Gerar Relatório", command=gerar_relatorio).pack(pady=10)
        tk.Button(self.frame_atual, text="Voltar", command=self.mostrar_menu_principal).pack(pady=10)
