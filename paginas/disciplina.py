import streamlit as st
import pandas as pd
import re
from core.db import registrar_resposta, registrar_comentario
 
def extrair_trechos(dados_linha):
    trechos = []
    for i in range(1, 7):  # trecho_1 a trecho_6
        campo = f"trecho_{i}"
        if pd.notna(dados_linha.get(campo, None)):
            texto = dados_linha[campo]
 
            # Converte **texto** em <strong>texto</strong> para negrito em HTML
            texto_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)
 
            trechos.append({
                "id": f"t{i}",
                "texto_html": texto_html
            })
    return trechos
 
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
 
    st.markdown(f"💬 **Explicação geral:** {dados_linha['bloco_explicacao']}")
    st.markdown("---")
 
    trechos = extrair_trechos(dados_linha)
 
    for trecho in trechos:
        col1, col2 = st.columns([5, 2])
 
        with col1:
            st.markdown(
                f"""
                <div style='text-align: justify; font-size: 16px;
                            padding-right: 20px; border-right: 1px solid #ccc;'>
                    {trecho['texto_html']}
                </div>
                """,
                unsafe_allow_html=True
            )
 
        with col2:
            key = f"radio_{nome_disciplina}_{trecho['id']}"
            escolha = st.radio(
                label="Validação:",
                options=["Não informado", "Aprovo", "Desaprovo"],
                key=key,
                horizontal=False
            )
 
            status = None
            if escolha == "Aprovo":
                status = "aprovo"
            elif escolha == "Desaprovo":
                status = "desaprovo"
 
            registrar_resposta(
                email=email,
                disciplina=nome_disciplina,
                trecho_id=trecho["id"],
                status=status
            )
 
        st.markdown("<hr>", unsafe_allow_html=True)
 
    comentario = st.text_area("📝 Comentário final (opcional):", key=f"comentario_{nome_disciplina}")
 
    if st.button("💾 Enviar comentário final"):
        registrar_comentario(email, nome_disciplina, comentario)
        st.success("Comentário salvo com sucesso.")
 
    if st.button("🔙 Voltar para lista de disciplinas"):
        st.session_state.pagina = "inicio"
        st.rerun()

