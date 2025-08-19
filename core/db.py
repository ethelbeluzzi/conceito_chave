# core/db.py
import streamlit as st
from datetime import datetime
from supabase import create_client, Client

@st.cache_resource
def conectar_supabase() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = conectar_supabase()

def registrar_resposta(email, disciplina, unidade, aula, trecho_id, status):
    if not email:
        return

    data = {
        "user_email": email,
        "disciplina": disciplina,
        "unidade": unidade,
        "aula": aula,
        "trecho_id": trecho_id,
        "status": status if status else None,
        "timestamp": datetime.utcnow().isoformat()
    }

    existente = supabase.table("validacoes") \
        .select("id") \
        .eq("user_email", email) \
        .eq("disciplina", disciplina) \
        .eq("unidade", unidade) \
        .eq("aula", aula) \
        .eq("trecho_id", trecho_id) \
        .execute()

    if existente.data:
        supabase.table("validacoes") \
            .update(data) \
            .eq("id", existente.data[0]["id"]) \
            .execute()
    else:
        supabase.table("validacoes") \
            .insert(data) \
            .execute()
