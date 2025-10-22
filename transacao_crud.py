from database import conectar
from datetime import datetime

# --- Funções CRUD para Transações ---

def adicionar_transacao(data, valor, tipo, categoria_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transacoes (data, valor, tipo, categoria_id) VALUES (?, ?, ?, ?)",
            (data, valor, tipo, categoria_id)
        )
        conn.commit()

def listar_transacoes():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.data, t.valor, t.tipo, c.nome
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria_id = c.id
            ORDER BY t.data DESC, t.id DESC
        """)
        return cursor.fetchall()

def buscar_transacao_por_id(id_transacao):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data, valor, tipo, categoria_id FROM transacoes WHERE id=?", (id_transacao,))
        transacao = cursor.fetchone()
        if transacao:
            data_str, valor, tipo, cat_id = transacao
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
            # Retorna um dicionário para facilitar o acesso no formulário
            return {'data': data_obj, 'valor': valor, 'tipo': tipo, 'cat_id': cat_id}
        return None

def atualizar_transacao(id_transacao, data, valor, tipo, categoria_id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE transacoes SET data=?, valor=?, tipo=?, categoria_id=? WHERE id=?",
            (data, valor, tipo, categoria_id, id_transacao)
        )
        conn.commit()

def excluir_transacao(id_transacao):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id=?", (id_transacao,))
        conn.commit()

