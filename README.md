### 💰 Controle Financeiro Pessoal

Um aplicativo simples para gerenciar suas finanças pessoais. Com ele, você pode:
✅ Cadastrar categorias (ex: Alimentação, Contas Fixas, Lazer).
✅ Registrar receitas e despesas.
✅ Ver o saldo total atualizado automaticamente.
✅ Gerar relatórios com gráficos para analisar seus gastos.

Tudo isso em uma interface gráfica desenvolvida com Tkinter e banco de dados SQLite.


🚀 Funcionalidades
📂 CRUD de Categorias: listar, adicionar, editar e excluir categorias.

📂 CRUD de Transações: registrar receitas e despesas com data, valor e categoria.

📊 Relatórios:

Filtro por intervalo de datas.

Gráfico em pizza (≤6 categorias) ou barras (>6 categorias).

🔄 Saldo Total atualizado em tempo real.

🗑️ Botão para resetar banco de dados (apaga todos os dados).

📦 Estrutura do Projeto
bash
Copiar
Editar
controle_financeiro/
│
├── main.py             # Arquivo principal para iniciar o app
├── telas.py            # Todas as telas (categorias, transações, relatórios)
├── database.py         # Conexão com o banco SQLite e criação de tabelas
├── banco.db            # Arquivo do banco de dados
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
⚙️ Requisitos
Python 3.8 ou superior instalado.

Pip para instalar dependências.

📥 Instalação
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/controle-financeiro.git
cd controle-financeiro
Crie um ambiente virtual (opcional, mas recomendado):

bash
Copiar
Editar
python -m venv venv
venv\Scripts\activate  # No Windows
source venv/bin/activate  # No Linux/Mac
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
▶️ Como Rodar
Execute o arquivo principal:

bash
Copiar
Editar
python main.py
A interface gráfica será aberta.

🗄️ Banco de Dados
O banco de dados é salvo no arquivo banco.db (SQLite).
Na primeira execução, as tabelas são criadas automaticamente.

🛠 Dependências
📄 requirements.txt

nginx
Copiar
Editar
tkcalendar
matplotlib
Instale com:

bash
Copiar
Editar
pip install -r requirements.txt
🖥️ Tecnologias Usadas
Python

Tkinter

SQLite

Tkcalendar

Matplotlib

