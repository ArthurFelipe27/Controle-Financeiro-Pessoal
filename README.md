# 💰 Controle Financeiro Pessoal

Um aplicativo simples para gerenciar suas finanças pessoais. Com ele, você pode:  
✅ Cadastrar categorias (ex: Alimentação, Contas Fixas, Lazer).  
✅ Registrar receitas e despesas.  
✅ Ver o saldo total atualizado automaticamente.  
✅ Gerar relatórios com gráficos para analisar seus gastos.  

Tudo isso em uma interface gráfica desenvolvida com Tkinter e banco de dados SQLite.


## 🚀 Funcionalidades
📂 CRUD de Categorias: listar, adicionar, editar e excluir categorias.  
📂 CRUD de Transações: registrar receitas e despesas com data, valor e categoria.  
📊 Relatórios:  
- Filtro por intervalo de datas.  
- Gráfico em pizza (≤6 categorias) ou barras (>6 categorias).
 
🔄 Saldo Total atualizado em tempo real.  
🗑️ Botão para resetar banco de dados (apaga todos os dados).  

## 📦 Estrutura do Projeto  

controle_financeiro/  
│   
├── main.py               **# Arquivo principal para iniciar o app**    
├── telas.py             **# Todas as telas (categorias, transações, relatórios)**      
├── database.py           **# Conexão com o banco SQLite e criação de tabelas**    
├── banco.db              **# Arquivo do banco de dados**    
├── requirements.txt      **# Dependências do projeto**    
└── README.md             **# Este arquivo**   

## ⚙️ Requisitos   
Python 3.8 ou superior instalado.  
Pip para instalar dependências.  

## 📥 Instalação  
1. Clone o repositório:  
```
git clone https://github.com/seu-usuario/controle-financeiro.git  
cd controle-financeiro
```
2. Crie um ambiente virtual (opcional, mas recomendado):
````
python -m venv venv
venv\Scripts\activate  # No Windows
source venv/bin/activate  # No Linux/Mac
````
3. Instale as dependências:
````
pip install -r requirementos.txt
````

## ▶️ Como Rodar
Execute o arquivo principal:
`python main.py`   
A interface gráfica será aberta.

## 🗄️ Banco de Dados  
O banco de dados é salvo no arquivo banco.db (SQLite).  
Na primeira execução, as tabelas são criadas automaticamente.  

## 🛠 Dependências  
📄 requirementos.txt  
- tkcalendar  
- matplotlib   

Instale com:  
``pip install -r requirementos.txt``

## 🖥️ Tecnologias Usadas
- Python  
- Tkinter  
- SQLite  
- Tkcalendar  
- Matplotlib  

