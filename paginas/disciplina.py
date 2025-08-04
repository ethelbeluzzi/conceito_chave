# paginas/disciplina.py
import streamlit as st
import pandas as pd
import re
 
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
 
    dados_linha = dados.iloc[0]
 
    st.markdown(f"💬 **Explicação geral:** {dados_linha['bloco_explicacao']}")
    st.markdown("---")
 
    trechos = extrair_trechos(dados_linha)
 
    for trecho in trechos:
        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"**{trecho['texto']}**")
        with col2:
            escolha = st.radio(
                f"Validação:",
                ["", "✅ Aprovo", "❌ Desaprovo"],
                key=f"{nome_disciplina}_{trecho['id']}"
            )
            # Aqui irá a chamada para o backend/Supabase
 
    st.markdown("---")
    comentario = st.text_area("📝 Comentário final (opcional):", key=f"comentario_{nome_disciplina}")
 
    # Botão de voltar
    if st.button("🔙 Voltar para lista de disciplinas"):
        st.session_state.pagina = "inicio"
        st.experimental_rerun()
