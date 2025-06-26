# PI-3-SEMESTRE
# 🍽️ Sistema de Controle de Refeições para Colaboradores

Projeto interdisciplinar do 3º semestre do curso de **Desenvolvimento de Software Multiplataforma (DSM)** da **FATEC Araras**, integrando os conhecimentos de **Gestão Ágil de Projetos**, **Desenvolvimento Web III** e **Banco de Dados Não Relacional**.

---

## 📘 Descrição

O sistema criado tem como principal objetivo controlar as refeições dos colaboradores de uma organização, automatizando o registro de consumo e facilitando a aplicação dos descontos na folha de pagamento de forma segura.

---

## 🚀 Funcionalidades

- Cadastro e autenticação de colaboradores
- Cadastro de restaurantes/obras/hotéis/usuários
- Registro e consulta de refeições consumidas
- Cálculo automático de valores a serem descontados
- Painel administrativo com dashboard de visualização
- Integração com banco de dados relacional e não relacional

---

## 🛠️ Tecnologias Utilizadas

- **Framework Web:** Django
- **Linguagem:** Python
- **Banco de Dados Relacional:** SQLite
- **Banco de Dados Não Relacional:** MongoDB
- **Padrão de Arquitetura:** MVT (Model-View-Template)
- **Gerenciamento Ágil:** Scrum

---

## 👩‍💻 Como Rodar o Projeto Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
# Ativar no Windows:
venv\Scripts\activate
# Ou no Linux/macOS:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o MongoDB

- Certifique-se de que o **MongoDB** está instalado e rodando localmente.
- O sistema conecta no MongoDB usando a URL padrão:
  ```
  mongodb://localhost:27017/
  ```
- Nome do banco: `refeicoes`  
- Nome da collection: `controle_diario`

> Você pode usar o [MongoDB Compass](https://www.mongodb.com/try/download/compass) para visualizar os dados.

### 5. Rode as migrações do Django
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor
```bash
python manage.py runserver
```

Depois, acesse:  
📍 `http://127.0.0.1:8000/` no navegador.

---

## 👥 Integrantes

- [Davi Samuel Schwartz](https://github.com/DaviSchwartz)
- [João Paulo Mussarelli Carossine](https://github.com/joaopcarossine)
- [Júlio Ryan Marsola](https://github.com/julioryanm)
- [Rayanne Gabriela Nunes](https://github.com/RayanneNunes)
- [Sara Beatriz Bento](https://github.com/SaraBeatris)

---
