# core/auth.py
import streamlit as st
from supabase import create_client

@st.cache_resource
def conectar_supabase_auth():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = conectar_supabase_auth()

def login_email():
    st.subheader("🔐 Login")
    email = st.text_input("Digite seu e-mail para entrar", key="email_input")
    if st.button("Enviar link de acesso"):
        if email:
            try:
                res = supabase.auth.sign_in_with_otp({"email": email})
                st.info("📩 Um link de acesso foi enviado para o seu e-mail.")
            except Exception as e:
                st.error(f"Erro ao enviar link: {e}")
        else:
            st.warning("Por favor, insira um e-mail válido.")

def verificar_sessao():
    """
    Retorna o e-mail do usuário logado ou None.
    """
    if "user_email" in st.session_state and st.session_state.user_email:
        return st.session_state.user_email
    
    return None
