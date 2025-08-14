# paginas/disciplina.py
import streamlit as st
import pandas as pd
from core.db import registrar_resposta, registrar_comentario

# Converte "\n" literais em quebras reais e mantém Markdown
def preparar_markdown(texto: str) -> str:
    if pd.isna(texto):
        return ""
    s = str(texto).replace("\r", "").strip()
    s = s.replace("\\n", "\n")  # converte literal \n em quebra real
    return s

# Página principal da disciplina
def pagina_disciplina(nome_disciplina: str):
    # Carrega os dados no formato: disciplina,unidade,aula,conteudo,trecho_1..trecho_6
    df = pd.read_csv("data/textos.csv")

    # Filtra pela disciplina
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

    # ==== Título da disciplina e info da unidade/aula ====
    st.markdown(f"<h2 style='margin-bottom:2px;'>{nome_disciplina}</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:20px; margin-bottom:20px;'>Unidade {dados_linha['unidade']} - Aula {dados_linha['aula']}</div>",
        unsafe_allow_html=True
    )

    # 1) Mensagem de instrução (menor que antes)
    st.markdown("<h4>🧾 Explicação geral</h4>", unsafe_allow_html=True)
    st.markdown(
        "A disciplina completa está abaixo. Depois, na seção de validação, você pode validar os negritos individualmente."
    )

    # 2) Texto completo (vem de 'conteudo')
    st.markdown("---")
    st.markdown("### 📚 Texto completo")

    texto_md = preparar_markdown(dados_linha["conteudo"])
    st.markdown(texto_md)

    # 3) Validação
    st.markdown("---")
    st.markdown("### ✅ Validação")

    for i in range(1, 7):
        campo = f"trecho_{i}"
        texto_trecho = dados_linha.get(campo, None)

        if pd.notna(texto_trecho) and str(texto_trecho).strip():
            col1, col2 = st.columns([5, 2])

            with col1:
                trecho_md = preparar_markdown(texto_trecho)
                st.markdown(trecho_md)

            with col2:
                escolha = st.radio(
                    label="Validação:",
                    options=["Não informado", "Aprovo", "Desaprovo"],
                    key=f"radio_{nome_disciplina}_t{i}",
                    horizontal=True,
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
                    status=status,
                )

            st.markdown("---")

    # 4) Comentário final
    comentario = st.text_area("📝 Comentário final (opcional):", key=f"comentario_{nome_disciplina}")

    if st.button("💾 Enviar comentário final"):
        registrar_comentario(email, nome_disciplina, comentario)
        st.success("Comentário salvo com sucesso.")

    if st.button("🔙 Voltar para lista de disciplinas"):
        st.session_state.pagina = "inicio"
        st.rerun()
