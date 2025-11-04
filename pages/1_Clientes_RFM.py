
import streamlit as st
import pandas as pd

st.title("Clientes e RFM")

uploaded = st.file_uploader("Faça upload da planilha de vendas", type=["xlsx"])
if uploaded:
    df = pd.read_excel(uploaded, engine="openpyxl")
    st.dataframe(df.head())
    st.success("Arquivo carregado com sucesso!")
