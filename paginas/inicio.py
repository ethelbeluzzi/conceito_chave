# paginas/inicio.py
import streamlit as st
import pandas as pd

# Carrega os dados do CSV com todas as colunas necessárias
def carregar_disciplinas():
    df = pd.read_csv("data/textos.csv")
    # Remove linhas sem disciplina
    df = df.dropna(subset=["disciplina"])
    return df

def pagina_inicio():
    st.title("Validação de Conteúdo por Disciplina")
    st.write("Selecione uma disciplina para validar os trechos destacados.")

    df = carregar_disciplinas()

    # Ordena por disciplina, unidade e aula
    df = df.sort_values(by=["disciplina", "unidade", "aula"])

    for _, row in df.iterrows():
        disciplina = row["disciplina"]
        unidade = row["unidade"]
        aula = row["aula"]

        # Botão com disciplina (destaque) + unidade/aula (menor)
        if st.button(
            f"📘 {disciplina}  —  Unidade {unidade}  |  Aula {aula}",
            key=f"btn_{disciplina}_{unidade}_{aula}"
        ):
            st.session_state.pagina = f"disciplina_{disciplina}"
            st.rerun()
