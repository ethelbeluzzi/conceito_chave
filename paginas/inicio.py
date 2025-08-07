# paginas/inicio.py
import streamlit as st
import pandas as pd
 
# Carrega os dados do CSV
def carregar_disciplinas():
    df = pd.read_csv("data/textos.csv")
    return df["disciplina"].dropna().unique()
 
def pagina_inicio():
    st.title("Validação de Conteúdo por Disciplina")
    st.write("Selecione uma disciplina para validar os trechos destacados.")
 
    disciplinas = carregar_disciplinas()
    for disciplina in sorted(disciplinas):
        if st.button(f"📘 {disciplina}"):
            st.session_state.pagina = f"disciplina_{disciplina}"
            st.rerun()
