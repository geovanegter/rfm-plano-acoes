
import streamlit as st
import pandas as pd

st.title("Kanban de Ações - Visual")

# Tenta carregar o arquivo, se não existir cria df vazio
try:
    df = pd.read_excel("planos_acoes.xlsx", engine="openpyxl")
except FileNotFoundError:
    df = pd.DataFrame(columns=["cliente", "acao", "status"])

status_colors = {"A Fazer":"#FFCC00", "Em andamento":"#00BFFF", "Concluído":"#00FF00"}

st.subheader("Arraste ou altere o status:")
for idx, row in df.iterrows():
    novo_status = st.selectbox(f"{row['cliente']} - {row['acao']}", list(status_colors.keys()), index=list(status_colors.keys()).index(row['status']))
    df.at[idx,'status'] = novo_status

if st.button("Salvar mudanças no Kanban"):
    df.to_excel("planos_acoes.xlsx", index=False)
    st.success("Mudanças salvas com sucesso!")
