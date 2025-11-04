
import streamlit as st

st.set_page_config(page_title="RFM SaaS V5", layout="wide")

# Toggle Light/Dark
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.title("Menu")
st.sidebar.button("Toggle Light/Dark", on_click=toggle_theme)

theme_bg = '#0E1117' if st.session_state.dark_mode else 'white'
theme_fg = 'white' if st.session_state.dark_mode else 'black'

st.markdown(f"<div style='color:{theme_fg};background-color:{theme_bg};padding:10px'>", unsafe_allow_html=True)
st.title("RFM SaaS - Dashboard & Kanban")
st.markdown("</div>", unsafe_allow_html=True)
