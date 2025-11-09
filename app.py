import streamlit as st
import pandas as pd
from lotofacil_utils import carregar_dados_reais

st.set_page_config(page_title="Estatísticas Lotofácil", layout="wide")

st.title("📊 Estatísticas da Lotofácil")

# Carregar dados reais ou do estado da sessão
if 'df_lotofacil' not in st.session_state:
    try:
        st.session_state.df_lotofacil = carregar_dados_reais()
    except Exception as e:
        st.error(f"Erro ao carregar dados reais: {e}")
        st.stop()

# Botão para atualizar jogos
if st.button("🔄 Atualizar jogos (baixar últimos resultados)"):
    try:
        st.session_state.df_lotofacil = carregar_dados_reais()
        st.success("Jogos atualizados com dados reais!")
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")

# Mostrar tabela de resultados
st.subheader("📅 Últimos resultados")
st.dataframe(st.session_state.df_lotofacil)

# Aqui você pode adicionar outras análises ou botões interativos
# Exemplo:
# - Estatísticas de números mais saídos
# - Relação com jogos anteriores
# - Números repetidos entre concursos
# - Sugestão de palpites
