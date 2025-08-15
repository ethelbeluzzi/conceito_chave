# paginas/inicio.py
import streamlit as st
import pandas as pd
import re

# Corrige campos como "Unidade 1" → 1
def extrair_numero(valor):
    if isinstance(valor, str):
        match = re.search(r"\d+", valor)
        return int(match.group()) if match else 0
    return int(valor)

def carregar_disciplinas():
    df = pd.read_csv("data/textos.csv")
    df = df.dropna(subset=["disciplina"])
    return df

def pagina_inicio():
    st.title("Validação de Conteúdo por Disciplina")
    st.write("Selecione uma aula dentro de cada disciplina para validar os trechos destacados.")

    df = carregar_disciplinas()
    disciplinas = df["disciplina"].unique()

    for disciplina in sorted(disciplinas):
        with st.expander(f"📘 {disciplina}"):
            df_disciplina = df[df["disciplina"] == disciplina]
            df_disciplina = df_disciplina.sort_values(by=["unidade", "aula"])

            cols = st.columns(4)  # cria primeira linha de 4 colunas
            col_index = 0

            for _, row in df_disciplina.iterrows():
                unidade = extrair_numero(row["unidade"])
                aula = extrair_numero(row["aula"])

                with cols[col_index]:
                    if st.button(
                        f"Unidade {unidade} | Aula {aula}",
                        key=f"{disciplina}_u{unidade}_a{aula}"
                    ):
                        st.session_state.pagina = f"disciplina_{disciplina}_u{unidade}_a{aula}"
                        st.rerun()

                col_index += 1
                if col_index == 4:
                    cols = st.columns(4)  # reinicia nova linha de 4 colunas
                    col_index = 0
