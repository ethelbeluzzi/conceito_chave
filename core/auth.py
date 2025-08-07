# core/auth.py
import streamlit as st
import pandas as pd
from supabase import create_client

@st.cache_resource
def conectar_supabase_auth():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = conectar_supabase_auth()

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

    if st.button("Enviar link de acesso"):
        if not email:
            st.warning("Por favor, insira um e-mail.")
            return

        if not email_autorizado(email):
            st.error("Este e-mail não está autorizado a acessar o sistema.")
            return

        try:
            supabase.auth.sign_in_with_otp({"email": email})
            st.success("📩 Link de acesso enviado! Verifique seu e-mail.")
        except Exception as e:
            st.error(f"Erro ao enviar link: {e}")

