# 💰 Controle Financeiro Pessoal
Um aplicativo simples e intuitivo para gerenciar suas finanças pessoais.
Com ele, você pode:

✅ Cadastrar categorias (ex: Alimentação, Contas Fixas, Lazer);  
✅ Registrar receitas e despesas;  
✅ Visualizar o saldo total atualizado automaticamente;  
✅ Gerar relatórios com gráficos para analisar seus gastos.  

Tudo isso em uma interface gráfica desenvolvida com Tkinter e banco de dados SQLite.

## 🚀 Funcionalidades

- CRUD de Categorias: Listar, adicionar, editar e excluir categorias;
- CRUD de Transações: Registrar receitas e despesas com data, valor e categoria;
- Relatórios Visuais: Filtrar por intervalo de datas e visualizar gráficos;
- Gráfico em pizza (≤ 6 categorias)
- Gráfico em barras (> 6 categorias)
- Saldo Total: Atualizado em tempo real;
- Reset do Banco: Botão para apagar todos os dados e começar do zero.

## 📦 Estrutura do Projeto
controle_financeiro/  
│  
├── main.py               # Arquivo principal para iniciar o app  
├── telas.py              # Lógica da interface gráfica (UI)  
├── database.py           # Conexão com o banco e criação/reset de tabelas  
├── categoria_crud.py     # Funções de acesso ao banco para categorias  
├── transacao_crud.py     # Funções de acesso ao banco para transações  
├── relatorio.py          # Geração de dados e gráficos dos relatórios  
├── banco.db              # Arquivo do banco de dados SQLite  
├── requirements.txt      # Dependências do projeto  
└── README.md             # Este arquivo  

## ⚙️ Requisitos

Python 3.8+

Pip (gerenciador de pacotes do Python)

## 📥 Instalação
1. Clone o repositório
````
git clone https://github.com/ArthurFelipe27/controle-financeiro.git
cd controle-financeiro
````
2. Crie e ative um ambiente virtual (recomendado)
````
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/Mac
python3 -m venv venv
source venv/bin/activate
````
3. Instale as dependências
````
pip install -r requirements.txt
````
## ⚠️ Solução de Problemas no Windows
Se aparecer o erro:  
> *Microsoft Visual C++ 14.0 or greater is required*  

Você precisa instalar as ferramentas de compilação da Microsoft:  
1. Baixe o instalador em [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/pt-br/downloads/?q=build+tools).  
2. Na aba “Cargas de Trabalho”, marque “Desenvolvimento para desktop com C++”.   
3. Instale e reinicie o computador.  
4. Tente novamente o comando de instalação das dependências.  

## ▶️ Como Rodar
Após instalar tudo, execute o aplicativo com:
``python main.py``
A interface gráfica será iniciada automaticamente.

## 🛠️ Tecnologias Usadas

- 🐍 Python
- 🪟 Tkinter (interface gráfica)
- 💾 SQLite (banco de dados local)
- 📅 Tkcalendar (seletor de datas)
- 📊 Matplotlib (gráficos e relatórios)

## 📸 Demonstração

<img width="350" height="150" alt="telainicial" src="https://github.com/user-attachments/assets/31d3719e-c0ad-41ba-819d-f23bc8261d79" />
<img width="350" height="150" alt="telagerenciartransacoes" src="https://github.com/user-attachments/assets/3313dfb4-07a8-45fd-8ee1-b21edec5f27c" />
<img width="350" height="150" alt="telagerenciarcategorias" src="https://github.com/user-attachments/assets/26b3fd15-2c67-421d-82a9-cb74ec3776bc" />
<img width="350" height="150" alt="telarelatorios" src="https://github.com/user-attachments/assets/cb31ac15-60b4-44fa-9007-b5394c8f7a59" />


### 🧑‍💻 Autor
Arthur Felipe  
📧 [arthurfelipedasilvamatosdev@gmail.com](mailto:arthurfelipedasilvamatosdev@gmail.com)  
🌐 [https://github.com/ArthurFelipe27](https://github.com/ArthurFelipe27)  
