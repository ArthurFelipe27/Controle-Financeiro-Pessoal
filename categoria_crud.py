import sqlite3
from database import conectar

# Este arquivo contém todas as funções de CRUD (Create, Read, Update, Delete)
# relacionadas às categorias. A lógica de banco de dados fica isolada aqui.

def listar_categorias():
    """Retorna uma lista de todas as categorias do banco."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM categorias ORDER BY nome")
        return cursor.fetchall()

def adicionar_categoria(nome):
    """Adiciona uma nova categoria, tratando exceções de nome duplicado."""
    if not nome or not nome.strip():
        raise ValueError("O nome da categoria não pode ser vazio.")
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome.strip(),))
            conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"A categoria '{nome}' já existe.")

def atualizar_categoria(id_categoria, novo_nome):
    """Atualiza o nome de uma categoria existente."""
    if not novo_nome or not novo_nome.strip():
        raise ValueError("O novo nome não pode ser vazio.")
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE categorias SET nome=? WHERE id=?", (novo_nome.strip(), id_categoria))
            conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"O nome '{novo_nome}' já está em uso por outra categoria.")

def excluir_categoria(id_categoria):
    """Exclui uma categoria do banco de dados."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categorias WHERE id=?", (id_categoria,))
        conn.commit()
