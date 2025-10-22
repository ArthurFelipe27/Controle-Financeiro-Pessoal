# 💰 Controle Financeiro Pessoal  
Um aplicativo simples para gerenciar suas finanças pessoais.   
Com ele, você pode:  
✅ Cadastrar categorias (ex: Alimentação, Contas Fixas, Lazer).  
✅ Registrar receitas e despesas.  
✅ Ver o saldo total atualizado automaticamente.  
✅ Gerar relatórios com gráficos para analisar seus gastos.Tudo isso em uma interface gráfica desenvolvida com Tkinter e banco de dados SQLite.  

## 🚀 Funcionalidades

- CRUD de Categorias: Listar, adicionar, editar e excluir categorias.
- CRUD de Transações: Registrar receitas e despesas com data, valor e categoria.
- Relatórios Visuais:Filtro por intervalo de datas.
- Gráfico em pizza (para ≤6 categorias) ou barras (>6 categorias).
- Saldo Total atualizado em tempo real.
- Reset do Banco: Um botão para apagar todos os dados e começar do zero.

## 📦 Estrutura do Projeto

controle_financeiro/
│
├── main.py               # Arquivo principal para iniciar o app
├── telas.py              # Lógica da interface gráfica (UI)
├── database.py           # Conexão com o banco e criação/reset de tabelas
├── categoria_crud.py     # Funções de acesso ao banco para categorias
├── transacao_crud.py     # Funções de acesso ao banco para transações
├── relatorio.py          # Lógica para gerar dados e gráficos dos relatórios
├── banco.db              # Arquivo do banco de dados SQLite
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo

## ⚙️ Requisitos
- Python 3.8 ou superior.
- Pip para instalar dependências.

## 📥 Instalação
1. Clone o repositório:
´´´´
git clone [https://github.com/seu-usuario/controle-financeiro.git](https://github.com/seu-usuario/controle-financeiro.git)
cd controle-financeiro
´´´´

2. Crie e ative um ambiente virtual (recomendado):

´´´´
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/Mac
source venv/bin/activate
´´´´

3. Instale as dependências a partir do arquivo requirements.txt:
´´´´pip install -r requirements.txt´´´´

⚠️ **Solução de Problemas no Windows** Se você receber um erro sobre *Microsoft Visual C++ 14.0 or greater is required* durante a instalação, significa que você precisa das ferramentas de compilação da Microsoft.

Baixe o instalador em **Microsoft C++ Build Tools**.
Execute-o e, na aba **"Cargas de Trabalho"**, selecione **"Desenvolvimento para desktop com C++"** e instale.
Após a instalação, reinicie o computador e tente instalar as dependências novamente.

## ▶️ Como Rodar
Com as dependências instaladas, execute o arquivo principal:
´´´´
python main.py
´´´´
A interface gráfica do programa será iniciada.

## 🛠️ Tecnologias Usadas
- Python
- Tkinter (para a interface gráfica)
- SQLite (para o banco de dados)
- Tkcalendar (para o seletor de datas)
- Matplotlib (para os gráficos)