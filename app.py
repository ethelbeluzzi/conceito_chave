# app.py
import streamlit as st
from core.auth import login_email, verificar_sessao

# Inicializa a página padrão
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# Verifica se o usuário está logado
user_email = verificar_sessao()
if not user_email:
    login_email()
    st.stop()

# Guarda o e-mail na sessão
st.session_state.user_email = user_email

# Navegação entre páginas
if st.session_state.pagina == "inicio":
    from paginas.inicio import pagina_inicio
    pagina_inicio()
elif st.session_state.pagina.startswith("disciplina_"):
    from paginas.disciplina import pagina_disciplina

    try:
        _, resto = st.session_state.pagina.split("disciplina_", 1)
        nome_raw, unidade_aula = resto.rsplit("_u", 1)
        unidade, aula = map(int, unidade_aula.split("_a"))
        nome_disciplina = nome_raw.strip()
        pagina_disciplina(nome_disciplina, unidade, aula)
    except Exception as e:
        st.error("Erro ao carregar a página da disciplina.")
        st.exception(e)
