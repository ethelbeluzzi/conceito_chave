# core/auth.py
import streamlit as st
import pandas as pd

def email_autorizado(email):
    try:
        df = pd.read_csv("data/emails_autorizados.csv")
        return email.strip().lower() in df["email"].str.lower().values
    except Exception as e:
        st.error(f"Erro ao carregar lista de e-mails autorizados: {e}")
        return False

def login_email():
    st.subheader("🔐 Login restrito")
    email = st.text_input("Digite seu e-mail institucional")

    if st.button("Entrar"):
        if not email:
            st.warning("Por favor, insira um e-mail.")
            return

        if not email_autorizado(email):
            st.error("Este e-mail não está autorizado a acessar o sistema.")
            return

        # Salva login na sessão
        st.session_state.user_email = email.strip().lower()
        st.session_state.pagina = "inicio"
        st.rerun()

def verificar_sessao():
    """
    Retorna o e-mail do usuário logado ou None.
    """
    return st.session_state.get("user_email", None)
