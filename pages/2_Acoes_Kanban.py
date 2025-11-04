
import streamlit as st
import pandas as pd

st.title("Kanban de Ações")

try:
    df = pd.read_excel("planos_acoes.xlsx", engine="openpyxl")
except FileNotFoundError:
    df = pd.DataFrame(columns=["cliente", "acao", "status"])

status_list = ["A Fazer", "Em andamento", "Concluído"]

for idx, row in df.iterrows():
    novo_status = st.selectbox(f"{row['cliente']} - {row['acao']}", status_list, index=status_list.index(row['status']))
    df.at[idx, 'status'] = novo_status

if st.button("Salvar mudanças no Kanban"):
    df.to_excel("planos_acoes.xlsx", index=False)
    st.success("Mudanças salvas com sucesso!")
