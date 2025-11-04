import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="ActionBI - RFM + Planos", layout="wide")

DATA_DIR = Path("data_files")
DATA_DIR.mkdir(exist_ok=True)

# default filenames inside the data directory
DEFAULT_VENDAS = DATA_DIR / "vendas_template.xlsx"
DEFAULT_PLANOS = DATA_DIR / "planos_acoes.xlsx"

# Helper functions
@st.cache_data
def load_vendas_from_file(file):
    df = pd.read_excel(file, engine="openpyxl")
    # ensure columns
    expected = ["cliente", "data", "valor", "colecao", "vendedor", "regional"]
    for c in expected:
        if c not in df.columns:
            st.error(f"Coluna esperada ausente: {c}")
            return pd.DataFrame(columns=expected)
    df["data"] = pd.to_datetime(df["data"])
    return df

def compute_rfm(df, reference_date=None):
    if reference_date is None:
        reference_date = df["data"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("cliente").agg({
        "data": lambda x: (reference_date - x.max()).days,
        "cliente": "count",
        "valor": "sum"
    }).rename(columns={"data":"recencia", "cliente":"frequencia", "valor":"monetario"}).reset_index()
    # quintiles 1-5 (5 best)
    r_labels = [5,4,3,2,1]  # lower recency (more recent) -> higher score
    rfm['R'] = pd.qcut(rfm['recencia'], 5, labels=r_labels)
    f_labels = [1,2,3,4,5]
    rfm['F'] = pd.qcut(rfm['frequencia'].rank(method='first'), 5, labels=f_labels)
    m_labels = [1,2,3,4,5]
    rfm['M'] = pd.qcut(rfm['monetario'], 5, labels=m_labels)
    rfm['R'] = rfm['R'].astype(int)
    rfm['F'] = rfm['F'].astype(int)
    rfm['M'] = rfm['M'].astype(int)
    rfm['score'] = rfm['R'] + rfm['F'] + rfm['M']
    # segment rules
    def segment(row):
        R,F,M = row['R'], row['F'], row['M']
        if R>=4 and F>=4 and M>=4:
            return "VIP"
        if F>=4 and M>=3:
            return "Frequentes"
        if M>=4 and F<=3:
            return "Valor Alto"
        if R<=2 and F<=3:
            return "Risco"
        if R==1 and M<=2:
            return "Dormant"
        if R>=4 and F==1:
            return "Novos"
        return "Outros"
    rfm['segmento'] = rfm.apply(segment, axis=1)
    return rfm

def load_planos(path):
    if not path.exists():
        df = pd.DataFrame(columns=["timestamp","cliente","vendedor","acao","prioridade","prazo","responsavel","status","observacao"])
        df.to_excel(path, index=False)
        return df
    return pd.read_excel(path, engine="openpyxl")

def append_plano(path, record):
    df = load_planos(path)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_excel(path, index=False)

# UI
st.title("ActionBI — RFM & Planos de Ação (MVP)")

col1, col2 = st.columns([1,1])

with col1:
    st.header("1) Carregar dados de vendas")
    uploaded = st.file_uploader("Carregue o Excel de vendas (ou deixe em branco para usar o template)", type=["xlsx"])
    if uploaded:
        vendas = load_vendas_from_file(uploaded)
    else:
        # try to use default file if exists in working dir (data_files), otherwise look for a top-level template
        if DEFAULT_VENDAS.exists():
            vendas = load_vendas_from_file(DEFAULT_VENDAS)
        else:
            st.info("Nenhum arquivo enviado e template não encontrado. Baixe o template e carregue-o.")
            vendas = pd.DataFrame(columns=["cliente","data","valor","colecao","vendedor","regional"])
    st.write("Amostra dos dados:")
    st.dataframe(vendas.head(10))

with col2:
    st.header("2) Planos de Ação")
    # ensure planos file exists in data_files
    planos_path = DEFAULT_PLANOS
    if not planos_path.exists():
        # create empty
        load_planos(planos_path)
    st.write("Planos existentes:")
    st.dataframe(load_planos(planos_path).tail(10))

st.markdown("---")

# RFM calculation
if vendas.shape[0] > 0:
    st.header("RFM — Segmentação automática")
    rfm = compute_rfm(vendas)
    # merge some info back: get vendedor/regional/colecao by most recent purchase per cliente
    latest = vendas.sort_values("data").groupby("cliente").last().reset_index()[["cliente","colecao","vendedor","regional"]]
    rfm = rfm.merge(latest, on="cliente", how="left")
    st.subheader("Tabela RFM")
    st.dataframe(rfm.sort_values("score", ascending=False).reset_index(drop=True))
    st.markdown("### Recomendações táticas por cliente")
    # táticas as per segment
    tactical_map = {
        "VIP":"Oferecer exclusividade (lançamento antecipado de coleção); Propor mix mais estratégico; Aumentar fidelização.",
        "Frequentes":"Focar em upsell e cross-sell; Sugerir novos produtos da coleção atual.",
        "Valor Alto":"Oferecer produtos premium; Priorizar visitas/contato do vendedor.",
        "Risco":"Ação de retenção; Contato ativo do vendedor; Oferta específica do mix que ele já compra.",
        "Dormant":"Campanha de reativação com incentivo comercial; Ação via marketing ou e-mail.",
        "Novos":"Onboarding comercial; Follow-up nos 30 primeiros dias; Garantir mix mínimo de entrada.",
        "Outros":"Analisar manualmente e definir plano de ação."
    }
    rfm["recomendacao"] = rfm["segmento"].map(tactical_map)
    st.dataframe(rfm[["cliente","R","F","M","score","segmento","recomendacao","vendedor","regional","colecao"]].sort_values("score", ascending=False).reset_index(drop=True))

    st.markdown("### Criar plano de ação")
    with st.form("plano_form", clear_on_submit=True):
        cliente_sel = st.selectbox("Cliente", rfm["cliente"].tolist())
        vendedor_default = rfm.loc[rfm["cliente"]==cliente_sel, "vendedor"].iloc[0]
        st.write("Vendedor:", vendedor_default)
        acao = st.text_area("Ação (descreva o que será feito)", height=120)
        prioridade = st.selectbox("Prioridade", ["Alta","Média","Baixa"])
        prazo = st.date_input("Prazo")
        responsavel = st.text_input("Responsável")
        status = st.selectbox("Status", ["Pendente","Em andamento","Concluído"])
        observacao = st.text_area("Observação (opcional)", height=80)
        submitted = st.form_submit_button("Salvar plano de ação")
        if submitted:
            record = {
                "timestamp": datetime.now().isoformat(),
                "cliente": cliente_sel,
                "vendedor": vendedor_default,
                "acao": acao,
                "prioridade": prioridade,
                "prazo": pd.to_datetime(prazo).date().isoformat(),
                "responsavel": responsavel,
                "status": status,
                "observacao": observacao
            }
            append_plano(planos_path, record)
            st.success("Plano de ação salvo em Excel.")
            st.experimental_rerun()
else:
    st.info("Carregue um arquivo de vendas para calcular RFM.")