# paginas/disciplina.py
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
            match = re.search(r"\*\*(.*?)\*\*", texto)
            if match:
                trechos.append({
                    "id": f"t{i}",
"texto": match.group(1),
                    "completo": texto
                })
    return trechos
 
def pagina_disciplina(nome_disciplina):
    st.title(f"📘 {nome_disciplina}")
    
    df = pd.read_csv("data/textos.csv")
    dados = df[df["disciplina"] == nome_disciplina]
 
    if dados.empty:
        st.error("Disciplina não encontrada.")
        return
 
    # Recupera e valida e-mail do usuário
    email = st.session_state.get("user_email", None)
    if not email:
        st.warning("Você precisa estar autenticado para validar os conteúdos.")
        return
 
    dados_linha = dados.iloc[0]
 
    st.markdown(f"💬 **Explicação geral:** {dados_linha['bloco_explicacao']}")
    st.markdown("---")
 
    trechos = extrair_trechos(dados_linha)
 
    for trecho in trechos:
        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"**{trecho['texto']}**")
        with col2:
            key_radio = f"{nome_disciplina}_{trecho['id']}"
            escolha = st.radio(
                label="Validação",
                options=["", "Aprovo", "Desaprovo"],
                key=key_radio,
                horizontal=True
            )
            # Salva no banco a cada mudança
            registrar_resposta(
                email=email,
                disciplina=nome_disciplina,
                trecho_id=trecho["id"],
                status=escolha.lower() if escolha else ""
            )
 
    st.markdown("---")
    comentario = st.text_area("📝 Comentário final (opcional):", key=f"comentario_{nome_disciplina}")
    if st.button("💾 Enviar comentário final"):
        registrar_comentario(email, nome_disciplina, comentario)
        st.success("Comentário salvo com sucesso.")
 
    if st.button("🔙 Voltar para lista de disciplinas"):
        st.session_state.pagina = "inicio"
        st.experimental_rerun()
