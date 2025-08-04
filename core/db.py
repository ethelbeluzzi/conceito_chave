# core/db.py
import os
from supabase import create_client, Client
from datetime import datetime
import streamlit as st
 
# Conecta ao Supabase com base nas variáveis do secrets.toml
@st.cache_resource
def conectar_supabase() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)
 
supabase = conectar_supabase()
 
# Função para gravar (ou atualizar) a resposta
def registrar_resposta(email, disciplina, trecho_id, status):
    if not email:
        return
 
    data = {
        "user_email": email,
        "disciplina": disciplina,
        "trecho_id": trecho_id,
        "status": status if status else None,
        "timestamp": datetime.utcnow().isoformat()
    }
 
    # Verifica se já existe
    existente = supabase.table("validacoes") \
        .select("id") \
        .eq("user_email", email) \
        .eq("disciplina", disciplina) \
        .eq("trecho_id", trecho_id) \
        .execute()
 
    if existente.data:
        # Atualiza
        supabase.table("validacoes") \
            .update(data) \
            .eq("id", existente.data[0]["id"]) \
            .execute()
    else:
        # Insere novo
        supabase.table("validacoes") \
            .insert(data) \
            .execute()
 
# Função para salvar o comentário final
def registrar_comentario(email, disciplina, comentario):
    if not comentario or not email:
        return
    data = {
        "user_email": email,
        "disciplina": disciplina,
        "trecho_id": "FINAL",
        "comentario_final": comentario,
        "timestamp": datetime.utcnow().isoformat()
    }
    supabase.table("validacoes").insert(data).execute()
