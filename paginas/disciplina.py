# paginas/disciplina.py
import streamlit as st
import pandas as pd
from core.db import registrar_resposta, registrar_comentario

def preparar_markdown(texto: str) -> str:
    if pd.isna(texto):
        return ""
    s = str(texto).replace("\r", "").strip()
    s = s.replace("\\n", "\n")
    return s

def pagina_disciplina(nome_disciplina: str, unidade: int, aula: int):
    df = pd.read_csv("data/textos.csv")

    # Limpeza defensiva
    df["disciplina"] = df["disciplina"].astype(str).str.strip()
    df["unidade"] = df["unidade"].astype(str).str.extract(r"(\d+)").astype(int)
    df["aula"] = df["aula"].astype(str).str.extract(r"(\d+)").astype(int)

    dados = df[
        (df["disciplina"] == nome_disciplina) &
        (df["unidade"] == unidade) &
        (df["aula"] == aula)
    ]

    if dados.empty:
        st.error("Disciplina não encontrada.")
        return

    email = st.session_state.get("user_email", None)
    if not email:
        st.warning("Você precisa estar autenticado.")
        return

    dados_linha = dados.iloc[0]

    # 1) Nome da disciplina
    st.markdown(f"<h2 style='margin-bottom:2px;'>{nome_disciplina}</h2>", unsafe_allow_html=True)

    # 2) Unidade - Aula
    st.markdown(
        f"<div style='font-size:20px; margin-bottom:20px;'>Unidade {unidade} - Aula {aula}</div>",
        unsafe_allow_html=True
    )
    
    # 3) Explicação geral
    st.markdown("<h4>🧾 Explicação geral</h4>", unsafe_allow_html=True) st.markdown("Esses são os conceitos-chave para validação. O texto completo da aula está abaixo para consulta.")

    st.markdown("---")

    # 4) Validação — "Conceitos-chave"
    st.markdown("### ✅ Conceitos-chave")
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
                    key=f"radio_{nome_disciplina}_u{unidade}_a{aula}_t{i}",
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

    # Comentário final opcional
    comentario = st.text_area(
        "📝 Comentário final (opcional):",
        key=f"comentario_{nome_disciplina}_u{unidade}_a{aula}"
    )
    if st.button("💾 Enviar comentário final"):
        registrar_comentario(email, nome_disciplina, comentario)
        st.success("Comentário salvo com sucesso.")

    st.markdown("---")

    # 4) Texto completo — "Texto completo da aula para consulta"
    st.markdown("### 📚 Texto completo da aula para consulta")
    texto_md = preparar_markdown(dados_linha["conteudo"])
    st.markdown(texto_md)

    # Navegação: Voltar / Próxima aula
    st.markdown("---")
    col_esq, col_dir = st.columns([1, 1])

    with col_esq:
        if st.button("🔙 Voltar para lista de disciplinas"):
            st.session_state.pagina = "inicio"
            st.rerun()

    with col_dir:
        df_disciplina = df[df["disciplina"] == nome_disciplina].sort_values(by=["unidade", "aula"])
        idx_atual = df_disciplina[
            (df_disciplina["unidade"] == unidade) &
            (df_disciplina["aula"] == aula)
        ].index

        if not idx_atual.empty:
            i = df_disciplina.index.get_loc(idx_atual[0])
            if i + 1 < len(df_disciplina):
                prox = df_disciplina.iloc[i + 1]
                prox_unidade = int(prox["unidade"])
                prox_aula = int(prox["aula"])

                if st.button("⏭️ Próxima aula da disciplina"):
                    st.session_state.pagina = f"disciplina_{nome_disciplina}_u{prox_unidade}_a{prox_aula}"
                    st.rerun()
            else:
                st.markdown("<p style='color:gray;'>✅ Última aula da disciplina.</p>", unsafe_allow_html=True)
