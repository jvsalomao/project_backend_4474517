# SGHSS - VidaPlus (Backend API)

API RESTful desenvolvida em **Python/Flask** para o Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS). Este projeto foca na segurança da informação, integridade de dados e conformidade rigorosa com a **LGPD** (Lei Geral de Proteção de Dados).

---

## 🚀 Funcionalidades Principais

### ✅ Gestão e Operação

- **Autenticação Segura**: Login via Token JWT (JSON Web Token) com expiração automática.
- **Gestão de Pacientes**: CRUD completo com criptografia de dados sensíveis (CPF e Histórico) em repouso.
- **Corpo Clínico**: Cadastro de médicos e gestão de agendas (dias e horários de atendimento).
- **Agendamento Inteligente**: Validação automática de disponibilidade na agenda do médico antes de marcar consultas.

### 📊 Inteligência de Negócio

- **Dashboard Gerencial**: Endpoint exclusivo que processa métricas em tempo real (KPIs de ocupação, taxas de cancelamento e totais operacionais).

### 🛡️ Segurança e LGPD

- **Criptografia Simétrica**: Uso da biblioteca _Fernet_ para proteger dados pessoais no banco.
- **Direito ao Esquecimento**: Rota para anonimização irreversível de dados a pedido do titular.
- **Portabilidade**: Exportação de dados pessoais em formato JSON.
- **Auditoria (Logs)**: Rastreabilidade completa de ações críticas (quem fez o quê e quando).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Framework**: Flask (Modularizado com Blueprints)
- **Banco de Dados**: SQLite (via SQLAlchemy ORM)
- **Segurança**:
  - `Flask-JWT-Extended` (Autenticação)
  - `Bcrypt` (Hashing de senhas)
  - `Cryptography/Fernet` (Dados sensíveis)

---

## 🔧 Estrutura do Projeto

A arquitetura foi desenhada para ser modular e escalável:

```text
SGHSS-VIDAPLUS/
│
├── app/
│   ├── models/
│   │   └── database.py       # Modelos do banco (SQLAlchemy)
│   ├── routes/
│   │   ├── auth.py           # Login e Registro
│   │   ├── patients.py       # Gestão de Pacientes (Criptografado)
│   │   ├── professionals.py  # Médicos e Agendas
│   │   ├── appointments.py   # Lógica de Agendamento
│   │   ├── admin.py          # Dashboard e Relatórios
│   │   └── security.py       # Logs e Rotas LGPD
│   └── __init__.py           # Configuração da App
│
├── instance/
│   └── hospital.db           # Banco de Dados (Gerado automaticamente)
├── app.py                    # Ponto de entrada
├── init_db.py                # Script de setup do banco
└── requirements.txt          # Dependências

```

---

## 🚀 Guia de Instalação e Execução

Siga os passos abaixo para configurar e rodar a API em um ambiente local de desenvolvimento.

### Pré-requisitos

- Python 3.10 ou superior
- Git instalado

### 1. Configurar o ambiente virtual

Recomendamos criar um ambiente virtual (`venv`) para isolar as dependências do projeto.

```bash

# No Windows (PowerShell ou CMD):

python -m venv venv
.\venv\Scripts\activate

# No Linux ou macOS:

python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Inicializar o banco de dados

```bash
python init_db.py
```

Este comando cria o arquivo `hospital.db` e gera o usuário Admin padrão.

### 4. Executar o servidor

```bash
python app.py
```

O servidor estará disponível em: `http://127.0.0.1:5000`

---

## 🔑 Credenciais de Acesso (Inicial)

Após rodar o script `init_db.py`, utilize as seguintes credenciais para obter o primeiro Token JWT:

- **Admin**: admin@vidaplus.com
- **Senha**: admin123

Nota: Para criar outros usuários (Médicos ou Pacientes), utilize a rota de registro da API (POST /api/auth/register).

---

## 📚 Documentação da API (Endpoints)

Todas as rotas protegidas exigem o cabeçalho Authorization: Bearer <seu_token>.

### 🔐 Autenticação

`POST /api/auth/register`

- Registrar novo usuário.

`POST /api/auth/login`

- Login e geração de Token.

### 🏥 Pacientes

`POST /api/patients/`

- Cadastrar paciente (CPF criptografado automaticamente).

`GET /api/patients/`

- Listar pacientes cadastrados.

### 👨‍⚕️ Profissionais e Agenda

`POST /api/professionals/`

- Cadastrar perfil médico.

`POST /api/professionals/{id}/schedule`

- Definir dias e horários de atendimento.

- Exemplo JSON: {"dia_semana": 0, "hora_inicio": "08:00", "hora_fim": "18:00"}

### 📅 Consultas

`POST /api/appointments/`

- Agendar consulta.

- Regra de Negócio: O sistema verifica a tabela Schedule e bloqueia se o médico não atender no dia/hora solicitados.

`GET /api/appointments/`

- Listar minhas consultas.

### 📈 Administrativo (Dashboard)

`GET /api/admin/dashboard-geral`

- Retorna JSON com estatísticas em tempo real:

- Total de Pacientes e Médicos.

- Consultas Pendentes vs. Realizadas.

- Taxa de Cancelamento (KPI).

### 🛡️ Segurança (LGPD)

`GET /api/security/logs`

- Visualizar logs de auditoria (Apenas Admin).

`GET /api/security/export-data`

- Exportar dados pessoais (Portabilidade).

`DELETE /api/security/delete-account`

- Anonimizar dados pessoais (Direito ao Esquecimento).

---

## 🧪 Como Testar (Postman)

**1. Login:** Realize uma requisição POST em `/api/auth/login` com as credenciais de Admin.

**2. Autenticação:** Copie o `access_token` da resposta. Nas próximas requisições, vá na aba Authorization, selecione Bearer Token e cole o código.

**3. Fluxo sugerido:**

- Criar Médico (POST /professionals).

- Definir Agenda (POST /schedule).

- Criar Paciente (POST /patients).

- Agendar Consulta (POST /appointments).

- Visualizar Dashboard (GET /dashboard-geral).

---

**Desenvolvido para fins acadêmicos - Curso de Análise e Desenvolvimento de Sistemas.**
