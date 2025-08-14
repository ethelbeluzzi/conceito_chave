# paginas/inicio.py
import streamlit as st
import pandas as pd

# Carrega todas as disciplinas com suas aulas
def carregar_disciplinas():
    df = pd.read_csv("data/textos.csv")
    df = df.dropna(subset=["disciplina"])
    return df

def pagina_inicio():
    st.title("Validação de Conteúdo por Disciplina")
    st.write("Selecione uma aula dentro de cada disciplina para validar os trechos destacados.")

    df = carregar_disciplinas()

    # Agrupa por disciplina
    disciplinas = df["disciplina"].unique()

    for disciplina in sorted(disciplinas):
        # Expander por disciplina
        with st.expander(f"📘 {disciplina}"):
            df_disciplina = df[df["disciplina"] == disciplina]
            df_disciplina = df_disciplina.sort_values(by=["unidade", "aula"])

            for _, row in df_disciplina.iterrows():
                unidade = row["unidade"]
                aula = row["aula"]

                if st.button(
                    f"Unidade {unidade} | Aula {aula}",
                    key=f"{disciplina}_u{unidade}_a{aula}"
                ):
                    # Página da disciplina agora precisa usar chave única por unidade/aula
                    st.session_state.pagina = f"disciplina_{disciplina}_u{unidade}_a{aula}"
                    st.rerun()

