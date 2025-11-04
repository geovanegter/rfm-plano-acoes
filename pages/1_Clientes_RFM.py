
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Clientes e RFM - Dashboard")

uploaded = st.file_uploader("Faça upload da planilha de vendas", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded, engine="openpyxl")
    st.subheader("Tabela de Clientes")
    st.dataframe(df)

    st.subheader("KPIs")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clientes", len(df))
    col2.metric("Receita Total", df['valor'].sum())
    col3.metric("Venda Média", round(df['valor'].mean(),2))

    st.subheader("Gráficos RFM")
    fig1 = px.histogram(df, x='valor', nbins=10, title="Distribuição de Valor")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df, x='cliente', y='valor', color='colecao', title="Valor por Cliente / Coleção")
    st.plotly_chart(fig2, use_container_width=True)
