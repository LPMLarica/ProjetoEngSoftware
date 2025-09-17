import streamlit as st
import pandas as pd
from datetime import datetime, date, time

st.set_page_config(page_title="Hospital Municipal", layout="wide")


if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=["Nome", "DataNascimento", "Telefone"])
if "profissionais" not in st.session_state:
    st.session_state.profissionais = pd.DataFrame(columns=["Nome", "Especialidade"])
if "consultas" not in st.session_state:
    st.session_state.consultas = pd.DataFrame(columns=["Paciente", "Profissional", "Data", "Hora", "Status", "Anotacoes"])
if "orcamentos" not in st.session_state:
    st.session_state.orcamentos = pd.DataFrame(columns=["Cliente", "Servico", "Valor", "Status"])
if "ordens" not in st.session_state:
    st.session_state.ordens = pd.DataFrame(columns=["Cliente", "Servico", "Status", "Historico"])

st.title("🏥 Sistema Hospitalar - Agenda e Ordens de Serviço")

menu = st.sidebar.radio("Menu", [
    "Cadastro de Pacientes",
    "Cadastro de Profissionais",
    "Agendamento de Consultas",
    "Gerenciar Consultas",
    "Orçamentos",
    "Ordens de Serviço"
])

# -------------------- Cadastro de Pacientes --------------------
if menu == "Cadastro de Pacientes":
    st.header("Cadastro de Pacientes")
    with st.form("form_paciente"):
        nome = st.text_input("Nome")
        nascimento = st.date_input("Data de Nascimento")
        telefone = st.text_input("Telefone")
        if st.form_submit_button("Cadastrar"):
            if nome.strip():
                st.session_state.pacientes.loc[len(st.session_state.pacientes)] = [nome.strip(), nascimento, telefone]
                st.success("Paciente cadastrado com sucesso!")
            else:
                st.error("Informe o nome do paciente.")
    st.subheader("Pacientes Cadastrados")
    st.dataframe(st.session_state.pacientes)


elif menu == "Cadastro de Profissionais":
    st.header("Cadastro de Profissionais")
    with st.form("form_profissional"):
        nome = st.text_input("Nome do Profissional")
        especialidade = st.text_input("Especialidade")
        if st.form_submit_button("Cadastrar"):
            if nome.strip():
                st.session_state.profissionais.loc[len(st.session_state.profissionais)] = [nome.strip(), especialidade.strip()]
                st.success("Profissional cadastrado com sucesso!")
            else:
                st.error("Informe o nome do profissional.")
    st.subheader("Profissionais Cadastrados")
    st.dataframe(st.session_state.profissionais)


elif menu == "Agendamento de Consultas":
    st.header("Agendar Consulta")
    if st.session_state.pacientes.empty or st.session_state.profissionais.empty:
        st.warning("Cadastre pacientes e profissionais antes de agendar consultas.")
    else:
        with st.form("form_agendamento"):
            paciente = st.selectbox("Paciente", st.session_state.pacientes["Nome"])
            profissional = st.selectbox("Profissional", st.session_state.profissionais["Nome"])
            data_consulta = st.date_input("Data", min_value=date.today())
            hora_consulta = st.time_input("Hora")
            if st.form_submit_button("Agendar"):
                conflito = (
                    (st.session_state.consultas["Profissional"] == profissional) &
                    (st.session_state.consultas["Data"] == data_consulta) &
                    (st.session_state.consultas["Hora"] == hora_consulta)
                ).any()
                if conflito:
                    st.error("Horário já ocupado para este profissional.")
                else:
                    st.session_state.consultas.loc[len(st.session_state.consultas)] = [
                        paciente, profissional, data_consulta, hora_consulta, "Agendado", ""
                    ]
                    st.success("Consulta agendada com sucesso!")
        st.subheader("Consultas Agendadas")
        st.dataframe(st.session_state.consultas)


elif menu == "Gerenciar Consultas":
    st.header("Gerenciar Consultas")
    if st.session_state.consultas.empty:
        st.info("Nenhuma consulta cadastrada.")
    else:
        for i, row in st.session_state.consultas.iterrows():
            with st.expander(f"{row['Data']} {row['Hora']} - {row['Paciente']} com {row['Profissional']}"):
                status = st.selectbox(
                    "Status",
                    ["Agendado", "Confirmado", "Cancelado", "Realizado"],
                    index=["Agendado", "Confirmado", "Cancelado", "Realizado"].index(row["Status"]),
                    key=f"status_consulta_{i}"
                )
                anotacoes = st.text_area("Anotações", row["Anotacoes"], key=f"anot_consulta_{i}")
                if st.button("Salvar", key=f"btn_salvar_consulta_{i}"):
                    st.session_state.consultas.at[i, "Status"] = status
                    st.session_state.consultas.at[i, "Anotacoes"] = anotacoes
                    st.success("Consulta atualizada!")


elif menu == "Orçamentos":
    st.header("Cadastro de Orçamentos")
    with st.form("form_orcamento"):
        cliente = st.text_input("Nome do Cliente")
        servico = st.text_input("Serviço/Procedimento")
        valor = st.number_input("Valor", min_value=0.0, step=0.01)
        if st.form_submit_button("Criar Orçamento"):
            if cliente.strip() and servico.strip():
                st.session_state.orcamentos.loc[len(st.session_state.orcamentos)] = [cliente.strip(), servico.strip(), valor, "Pendente"]
                st.success("Orçamento criado!")
            else:
                st.error("Preencha todos os campos.")
    st.subheader("Orçamentos")
    for i, row in st.session_state.orcamentos.iterrows():
        cols = st.columns([2, 2, 1, 1])
        cols[0].write(row["Cliente"])
        cols[1].write(row["Servico"])
        cols[2].write(f"R$ {row['Valor']:.2f}")
        novo_status = cols[3].selectbox(
            "Status",
            ["Pendente", "Aprovado", "Reprovado"],
            index=["Pendente", "Aprovado", "Reprovado"].index(row["Status"]),
            key=f"status_orc_{i}"
        )
        if novo_status != row["Status"]:
            st.session_state.orcamentos.at[i, "Status"] = novo_status
            if novo_status == "Aprovado":
                ja_existe_os = (
                    (st.session_state.ordens["Cliente"] == row["Cliente"]) &
                    (st.session_state.ordens["Servico"] == row["Servico"])
                ).any()
                if not ja_existe_os:
                    st.session_state.ordens.loc[len(st.session_state.ordens)] = [
                        row["Cliente"], row["Servico"], "Em execução", "Ordem criada a partir do orçamento"
                    ]
            st.success("Status atualizado!")


elif menu == "Ordens de Serviço":
    st.header("Ordens de Serviço")
    if st.session_state.ordens.empty:
        st.info("Nenhuma OS criada.")
    else:
        for i, row in st.session_state.ordens.iterrows():
            with st.expander(f"{row['Cliente']} - {row['Servico']} ({row['Status']})"):
                status = st.selectbox(
                    "Status",
                    ["Aguardando peças", "Em execução", "Finalizado"],
                    index=["Aguardando peças", "Em execução", "Finalizado"].index(row["Status"]),
                    key=f"status_os_{i}"
                )
                historico = st.text_area("Histórico", row["Historico"], key=f"hist_os_{i}")
                if st.button("Salvar", key=f"btn_os_{i}"):
                    st.session_state.ordens.at[i, "Status"] = status
                    st.session_state.ordens.at[i, "Historico"] = historico
                    st.success("OS atualizada!")
    st.subheader("Lista de OS")
    st.dataframe(st.session_state.ordens)