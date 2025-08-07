import streamlit as st
import pandas as pd
import re
from core.db import registrar_resposta, registrar_comentario
 
# Formata o texto substituindo **negrito** por <strong> e mantendo parágrafos
def formatar_html(texto):
    if pd.isna(texto):
        return ""
    texto = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)  # Negrito
    texto = texto.replace("\r", "")  # Remove quebras de carroça
    texto = texto.strip()
    texto = texto.replace("\n\n", "</p><p>")  # Parágrafos
    texto = texto.replace("\n", " ")  # Quebras simples viram espaço
    return f"<p>{texto}</p>"
 
# Página principal da disciplina
def pagina_disciplina(nome_disciplina):
    st.title(f"📘 {nome_disciplina}")
 
    # Carrega os dados
    df = pd.read_csv("data/textos.csv")
    dados = df[df["disciplina"] == nome_disciplina]
 
    if dados.empty:
        st.error("Disciplina não encontrada.")
        return
 
    # Verifica autenticação
    email = st.session_state.get("user_email", None)
    if not email:
        st.warning("Você precisa estar autenticado.")
        return
 
    dados_linha = dados.iloc[0]
 
    # 1. Mensagem de instrução
    st.markdown("### 🧾 Explicação geral")
    st.markdown("A disciplina completa está abaixo. Depois, na seção de validação, você pode validar os negritos individualmente.")
 
    # 2. Texto completo (renderizado com HTML)
    st.markdown("---")
    st.markdown("### 📚 Texto completo")
 
    texto_html = formatar_html(dados_linha["bloco_explicacao"])
    st.markdown(texto_html, unsafe_allow_html=True)
 
    # 3. Validação
    st.markdown("---")
    st.markdown("### ✅ Validação")
 
    for i in range(1, 7):
        campo = f"trecho_{i}"
        texto_trecho = dados_linha.get(campo, None)
 
        if pd.notna(texto_trecho):
            col1, col2 = st.columns([5, 2])
 
            with col1:
                trecho_html = formatar_html(texto_trecho)
                st.markdown(trecho_html, unsafe_allow_html=True)
 
            with col2:
                escolha = st.radio(
                    label="Validação:",
                    options=["Não informado", "Aprovo", "Desaprovo"],
                    key=f"radio_{nome_disciplina}_t{i}",
                    horizontal=True
                )
 
                status = None
                if escolha == "Aprovo":
                    status = "aprovo"
                elif escolha == "Desaprovo":
                    status = "desaprovo"
 
                registrar_resposta(
                    email=email,
                    disciplina=nome_disciplina,
                    trecho_id=f"t{i}",
                    status=status
                )
 
            st.markdown("---")
 
    # 4. Comentário final
    comentario = st.text_area("📝 Comentário final (opcional):", key=f"comentario_{nome_disciplina}")
 
    if st.button("💾 Enviar comentário final"):
        registrar_comentario(email, nome_disciplina, comentario)
        st.success("Comentário salvo com sucesso.")
 
    if st.button("🔙 Voltar para lista de disciplinas"):
        st.session_state.pagina = "inicio"
        st.rerun()
