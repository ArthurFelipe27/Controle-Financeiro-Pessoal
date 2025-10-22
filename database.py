import sqlite3
from contextlib import contextmanager

DB_NAME = "banco.db"

@contextmanager
def conectar():
    """
    Conecta ao banco de dados SQLite como um gerenciador de contexto.
    Isso garante que a conexão seja aberta e fechada de forma segura e automática.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        yield conn
    except sqlite3.Error as e:
        print(f"Erro na conexão com o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def criar_tabelas():
    """
    Cria as tabelas 'categorias' e 'transacoes' se elas ainda não existirem.
    Insere categorias padrão na primeira execução.
    """
    with conectar() as conn:
        cursor = conn.cursor()

        # Tabela de categorias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """)

        # Tabela de transações
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('Receita', 'Despesa')),
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE SET NULL
        )
        """)

        # Insere categorias padrão se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM categorias")
        if cursor.fetchone()[0] == 0:
            categorias_padrao = [
                ("Alimentação",), ("Contas Básicas",), ("Transporte",),
                ("Lazer",), ("Salário",), ("Outros",)
            ]
            cursor.executemany("INSERT INTO categorias (nome) VALUES (?)", categorias_padrao)
            print("Categorias padrão adicionadas ao banco.")

        conn.commit()

def resetar_banco():
    """
    Apaga completamente as tabelas existentes e as recria com os dados padrão.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS transacoes")
        cursor.execute("DROP TABLE IF EXISTS categorias")
        conn.commit()
    criar_tabelas()
    print("Banco de dados resetado com sucesso.")

