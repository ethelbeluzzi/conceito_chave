import streamlit as st
import pandas as pd
import re
from core.db import registrar_resposta, registrar_comentario
 
# Converte **...** para <strong>...</strong> em HTML
def formatar_com_negrito(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)
 
# Página principal da disciplina
def pagina_disciplina(nome_disciplina):
    st.title(f"📘 {nome_disciplina}")
 
    df = pd.read_csv("data/textos.csv")
    dados = df[df["disciplina"] == nome_disciplina]
 
    if dados.empty:
        st.error("Disciplina não encontrada.")
        return
 
    email = st.session_state.get("user_email", None)
    if not email:
        st.warning("Você precisa estar autenticado.")
        return
 
    dados_linha = dados.iloc[0]
 
    # 1. Explicação geral (texto completo com negrito já incluso)
    st.markdown("### 🧾 Explicação geral")
    texto_html = formatar_com_negrito(dados_linha["bloco_explicacao"])
 
    st.markdown(
        f"<div style='text-align: justify; font-size: 16px'>{texto_html}</div>",
        unsafe_allow_html=True
    )
 
    # 2. Seção de validação
    st.markdown("---")
    st.markdown("### ✅ Validação")
 
    # Itera sobre os trechos 1 a 6
    for i in range(1, 7):
        campo = f"trecho_{i}"
        texto_trecho = dados_linha.get(campo, None)
 
        if pd.notna(texto_trecho):
            col1, col2 = st.columns([5, 2])
 
            with col1:
                st.markdown(f"<div style='font-size: 16px'>{formatar_com_negrito(texto_trecho)}</div>", unsafe_allow_html=True)
 
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
 
    # Comentário final
    comentario = st.text_area("📝 Comentário final (opcional):", key=f"comentario_{nome_disciplina}")
 
    if st.button("💾 Enviar comentário final"):
        registrar_comentario(email, nome_disciplina, comentario)
        st.success("Comentário salvo com sucesso.")
 
    if st.button("🔙 Voltar para lista de disciplinas"):
        st.session_state.pagina = "inicio"
        st.rerun()
