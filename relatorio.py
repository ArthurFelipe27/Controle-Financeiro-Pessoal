from database import conectar
import matplotlib.pyplot as plt

# Este arquivo contém a lógica para buscar dados e gerar gráficos para os relatórios.

def get_dados_relatorio(data_inicio, data_fim):
    """Busca os dados consolidados de receitas e despesas em um período."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tipo, COALESCE(SUM(valor), 0) FROM transacoes
            WHERE data BETWEEN ? AND ?
            GROUP BY tipo
        """, (data_inicio, data_fim))
        dados = dict(cursor.fetchall())
        receitas = dados.get('Receita', 0)
        despesas = dados.get('Despesa', 0)
        return receitas, despesas

def get_despesas_por_categoria(data_inicio, data_fim):
    """Busca as despesas agrupadas por categoria em um período."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nome, SUM(t.valor) FROM transacoes t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.tipo='Despesa' AND t.data BETWEEN ? AND ?
            GROUP BY c.nome
            ORDER BY SUM(t.valor) DESC
        """, (data_inicio, data_fim))
        return cursor.fetchall()

def gerar_grafico_despesas(categorias):
    """
    Gera e exibe um gráfico de pizza ou de barras com base nos dados
    de despesas por categoria.
    """
    if not categorias:
        return False # Indica que não há dados para exibir

    nomes, valores = zip(*categorias)

    plt.figure(figsize=(10, 6))
    
    # Decide entre gráfico de pizza (poucas categorias) e barras (muitas)
    if len(nomes) <= 6:
        plt.title("Despesas por Categoria (Pizza)")
        plt.pie(valores, labels=nomes, autopct="%1.1f%%", startangle=140,
                wedgeprops=dict(width=0.4), pctdistance=0.8)
        plt.axis("equal")
    else:
        plt.title("Despesas por Categoria (Barras)")
        plt.barh(nomes, valores, color="skyblue")
        plt.xlabel("Valor Gasto (R$)")
        plt.gca().invert_yaxis() # A maior barra fica no topo

    plt.tight_layout()
    plt.show()
    return True # Indica que o gráfico foi gerado
