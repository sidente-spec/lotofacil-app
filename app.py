import streamlit as st
import pandas as pd
from lotofacil_utils import carregar_dados, atualizar_jogos

# Inicializa dados na sessão
if 'df_lotofacil' not in st.session_state:
    st.session_state.df_lotofacil = carregar_dados()

st.title("Análise Avançada da Lotofácil")

# Botão para atualizar os jogos
if st.button("Atualizar jogos (baixar últimos resultados)"):
    st.session_state.df_lotofacil = atualizar_jogos()
    st.success("Jogos atualizados!")

df = st.session_state.df_lotofacil

# Seleção de número de sorteios para análise
num_sorteios = st.slider("Quantos últimos sorteios considerar?", min_value=2, max_value=len(df), value=10)
ultimos_sorteios = df.tail(num_sorteios).reset_index(drop=True)

st.subheader(f"Últimos {num_sorteios} sorteios")
st.dataframe(ultimos_sorteios)

# Botão para números repetidos entre os 2 últimos sorteios
if st.button("Mostrar números repetidos entre os 2 últimos sorteios"):
    if len(ultimos_sorteios) < 2:
        st.warning("Escolha pelo menos 2 sorteios.")
    else:
        ultimo = set(ultimos_sorteios.iloc[-1][2:])
        penultimo = set(ultimos_sorteios.iloc[-2][2:])
        repetidos = sorted(ultimo.intersection(penultimo))
        st.write(f"Números repetidos: {repetidos if repetidos else 'Nenhum'}")

# Escolha de números de confiança do usuário
st.subheader("Escolha seus números de confiança")
col1, col2 = st.columns(2)
with col1:
    nums_vao_sair = st.multiselect("Números que você acredita que vão sair:", options=list(range(1,26)))
with col2:
    nums_nao_sair = st.multiselect("Números que você acredita que NÃO vão sair:", options=list(range(1,26)))

# Validação
if set(nums_vao_sair).intersection(set(nums_nao_sair)):
    st.error("Erro: um número não pode estar em ambos os grupos.")
else:
    st.subheader("Sugestões baseadas nas suas escolhas")
    todos_numeros = ultimos_sorteios.iloc[:, 2:].values.flatten()
    freq = pd.Series(todos_numeros).value_counts().sort_index()

    df_freq = pd.DataFrame({
        'Número': range(1, 26),
        'Frequência': [freq.get(num, 0) for num in range(1, 26)]
    })

    # Filtros do usuário
    if nums_vao_sair:
        df_freq.loc[~df_freq['Número'].isin(nums_vao_sair), 'Frequência'] = 0
    if nums_nao_sair:
        df_freq.loc[df_freq['Número'].isin(nums_nao_sair), 'Frequência'] = 0

    df_freq = df_freq.sort_values(by='Frequência', ascending=False).reset_index(drop=True)
    st.write("Frequência ajustada:")
    st.dataframe(df_freq)

    sugestao = df_freq[df_freq['Frequência'] > 0]['Número'].tolist()
    if len(sugestao) >= 15:
        sugestao = sugestao[:15]
        st.success(f"Sugestão de 15 números: {sugestao}")
    else:
        st.warning("Não há números suficientes após aplicar os filtros.")

# Análise visual de repetição geral
st.subheader("Números que mais se repetem entre os últimos sorteios")
repetidos_geral = pd.Series(ultimos_sorteios.iloc[:, 2:].values.flatten()).value_counts()
st.bar_chart(repetidos_geral)
