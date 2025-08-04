# app.py
import streamlit as st
 
# Inicializa a página padrão
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
 
# Navega conforme o estado
if st.session_state.pagina == "inicio":
    from paginas.inicio import pagina_inicio
    pagina_inicio()
elif st.session_state.pagina.startswith("disciplina_"):
    from paginas.disciplina import pagina_disciplina
    nome_disciplina = st.session_state.pagina.split("_", 1)[1]
    pagina_disciplina(nome_disciplina)
