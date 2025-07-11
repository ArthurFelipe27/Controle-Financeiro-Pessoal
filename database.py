import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela categorias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    # Tabela transações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        valor REAL NOT NULL,
        tipo TEXT NOT NULL,  -- Receita ou Despesa
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )
    """)

    # Inserir categorias padrão se estiver vazio
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        categorias_padrao = [
            ("Alimentação",),
            ("Contas Básicas",),
            ("Transporte",),
            ("Lazer",),
            ("Salário",),
            ("Outros",)
        ]
        cursor.executemany("INSERT INTO categorias (nome) VALUES (?)", categorias_padrao)
        print("Categorias padrão adicionadas ao banco.")

    conn.commit()
    conn.close()

def resetar_banco():
    """Apaga todas as tabelas e recria com categorias padrão"""
    conn = conectar()
    cursor = conn.cursor()

    # Apagar tabelas
    cursor.execute("DROP TABLE IF EXISTS transacoes")
    cursor.execute("DROP TABLE IF EXISTS categorias")

    conn.commit()
    conn.close()

    # Recriar tabelas e categorias padrão
    criar_tabelas()
    print("Banco resetado com categorias padrão.")
