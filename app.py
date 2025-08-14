# app.py
import streamlit as st
from core.auth import login_email, verificar_sessao
import re

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
        # Exemplo: "disciplina_Direção de Arte_u1_a3"
        pagina_raw = st.session_state.pagina.replace("disciplina_", "")

        # Regex para extrair: nome, unidade e aula
        match = re.match(r"(.+)_u(\d+)_a(\d+)", pagina_raw)

        if match:
            nome_disciplina = match.group(1).strip()
            unidade = int(match.group(2))
            aula = int(match.group(3))
            pagina_disciplina(nome_disciplina, unidade, aula)
        else:
            st.error("Formato inválido para nome da página.")
    except Exception as e:
        st.error("Erro ao carregar a página da disciplina.")
        st.exception(e)
