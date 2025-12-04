Hospital Management System – Streamlit Application

Agenda Médica, Ordens de Serviço e Orçamentos

Este projeto é um Sistema Hospitalar Web desenvolvido em Python + Streamlit, que permite gerenciar:

Cadastro de Pacientes

Cadastro de Profissionais de Saúde

Agendamento de Consultas

Gerenciamento de Consultas

Criação e Controle de Orçamentos

Ordens de Serviço (OS)

Tudo isso de forma simples, intuitiva e sem banco de dados externo — todos os dados ficam em memória através do st.session_state.

📌 Funcionalidades Principais
✅ 1. Cadastro de Pacientes

Permite registrar informações como:

Nome

Data de Nascimento

Telefone

Os pacientes são listados automaticamente em uma tabela visual.

✅ 2. Cadastro de Profissionais

Registra profissionais com:

Nome

Especialidade

Esses dados são utilizados no agendamento de consultas.

✅ 3. Agendamento de Consultas

Permite escolher:

Paciente

Profissional

Data

Hora

O sistema inclui validação para evitar conflitos de horário para o mesmo profissional.

✅ 4. Gerenciamento de Consultas

Permite:

Atualizar status (Agendado, Confirmado, Cancelado, Realizado)

Inserir anotações

Editar cada consulta individualmente

✅ 5. Módulo de Orçamentos

Criação de orçamentos contendo:

Cliente

Serviço/Procedimento

Valor

Status (Pendente, Aprovado, Reprovado)

Quando um orçamento é aprovado, automaticamente é criada uma Ordem de Serviço vinculada.

✅ 6. Ordens de Serviço (OS)

Após aprovação de um orçamento, a OS é criada com:

Cliente

Serviço

Status (Aguardando Peças, Em Execução, Finalizado)

Histórico de atividades

Tudo pode ser atualizado diretamente pela interface.

🧱 Arquitetura do Código

O sistema utiliza o st.session_state como mini banco de dados em memória:

Tabela	Campos
pacientes	Nome, DataNascimento, Telefone
profissionais	Nome, Especialidade
consultas	Paciente, Profissional, Data, Hora, Status, Anotacoes
orcamentos	Cliente, Servico, Valor, Status
ordens	Cliente, Servico, Status, Historico

Cada módulo do menu manipula essas tabelas usando formulários e tabelas exibidas com Streamlit.

⚙️ Instalação
🔹 1. Requisitos

Certifique-se que você tem instalado:

Python 3.8+

pip atualizado

🔹 2. Criar ambiente virtual (opcional, mas recomendado)
Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

🔹 3. Instalar dependências necessárias
pip install streamlit pandas

▶️ Como Rodar o Sistema

Dentro da pasta do projeto, execute:

streamlit run app.py


(considerando que o arquivo principal se chama app.py)

O sistema abrirá automaticamente em:

http://localhost:8501

🧭 Como Navegar pela Aplicação

A interface possui um menu lateral com:

Cadastro de Pacientes

Cadastro de Profissionais

Agendamento de Consultas

Gerenciar Consultas

Orçamentos

Ordens de Serviço

Cada módulo abre uma interface específica para inserir dados, visualizar tabelas e atualizar registros.

📁 Estrutura Recomendada do Projeto
hospital-system/
│── app.py
│── README.md
│── requirements.txt


🎉 Conclusão

Este sistema serve como base para aplicações clínicas e hospitalares simples, oferecendo um fluxo completo: cadastro → agendamento → orçamento → ordem de serviço, tudo em um único ambiente Streamlit.
