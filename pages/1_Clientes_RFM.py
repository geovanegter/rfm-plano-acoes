
import streamlit as st
import pandas as pd

st.title("Clientes e RFM - Dashboard")

uploaded = st.file_uploader("Faça upload da planilha de vendas", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded, engine="openpyxl")
    st.subheader("Tabela de Clientes")
    st.dataframe(df)

    # Salvar vendas
    df.to_excel("vendas.xlsx", index=False)

    # Atualizar Kanban automaticamente
    try:
        kanban_df = pd.read_excel("planos_acoes.xlsx", engine="openpyxl")
    except FileNotFoundError:
        kanban_df = pd.DataFrame(columns=["cliente","acao","status"])

    for cliente in df['cliente']:
        if cliente not in kanban_df['cliente'].values:
            kanban_df = pd.concat([kanban_df, pd.DataFrame([{"cliente":cliente,"acao":"Ligar","status":"A Fazer"}])], ignore_index=True)
            kanban_df = pd.concat([kanban_df, pd.DataFrame([{"cliente":cliente,"acao":"Enviar e-mail","status":"A Fazer"}])], ignore_index=True)

    kanban_df.to_excel("planos_acoes.xlsx", index=False)
    st.success("Vendas salvas e Kanban atualizado!")

    # KPIs básicos
    st.subheader("KPIs")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clientes", len(df))
    col2.metric("Receita Total", df['valor'].sum())
    col3.metric("Venda Média", round(df['valor'].mean(),2))

    # Gráficos RFM
    import plotly.express as px
    st.subheader("Gráficos RFM")
    fig1 = px.histogram(df, x='valor', nbins=10, title="Distribuição de Valor")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df, x='cliente', y='valor', color='colecao', title="Valor por Cliente / Coleção")
    st.plotly_chart(fig2, use_container_width=True)
