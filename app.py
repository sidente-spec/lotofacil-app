import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Função simulada para carregar dados da Lotofácil
def carregar_dados():
    np.random.seed(42)
    sorteios = []
    datas = []
    base_date = datetime.today() - timedelta(days=100*3)  # 3 dias entre sorteios, exemplo
    for i in range(100):
        numeros = sorted(np.random.choice(range(1, 26), 15, replace=False))
        sorteios.append(numeros)
        datas.append(base_date + timedelta(days=i*3))
    df = pd.DataFrame(sorteios, columns=[f'Num{i+1}' for i in range(15)])
    df['Concurso'] = range(1, 101)
    df['Data'] = pd.to_datetime(datas).dt.date
    # Reorganiza colunas para Concurso e Data primeiro
    colunas = ['Concurso', 'Data'] + [f'Num{i+1}' for i in range(15)]
    df = df[colunas]
    return df

# Função para atualizar (recarregar) os dados - pode ser substituída para baixar da internet
def atualizar_jogos():
    # Aqui você colocaria o código que atualiza a base real (download + processamento)
    # Por enquanto, só recarrega os dados simulados:
    return carregar_dados()

# Variável de sessão para armazenar os dados atualizados
if 'df_lotofacil' not in st.session_state:
    st.session_state.df_lotofacil = carregar_dados()

st.title("Análise Avançada da Lotofácil")

# Botão para atualizar os jogos
if st.button("Atualizar jogos (baixar últimos resultados)"):
    st.session_state.df_lotofacil = atualizar_jogos()
    st.success("Jogos atualizados!")

df = st.session_state.df_lotofacil

# Seleção do número de sorteios para análise
num_sorteios = st.slider("Quantos últimos sorteios considerar para análise?", min_value=2, max_value=len(df), value=10)

# Filtra os últimos sorteios e exibe com concurso e data
ultimos_sorteios = df.tail(num_sorteios).reset_index(drop=True)

st.subheader(f"Últimos {num_sorteios} sorteios")
st.dataframe(ultimos_sorteios)

# Botão para números repetidos do último sorteio para o anterior
if st.button("Mostrar números repetidos entre os 2 últimos sorteios"):
    if len(ultimos_sorteios) < 2:
        st.warning("Escolha pelo menos 2 sorteios para essa análise.")
    else:
        ultimo = set(ultimos_sorteios.iloc[-1][2:])  # ignorar Concurso e Data
        penultimo = set(ultimos_sorteios.iloc[-2][2:])
        repetidos = sorted(ultimo.intersection(penultimo))
        st.write(f"Números repetidos entre último e penúltimo sorteio: {repetidos if repetidos else 'Nenhum número repetido'}")

# Escolha dos números que o usuário acredita que vão sair e que não vão sair
st.subheader("Escolha seus números de confiança")

col1, col2 = st.columns(2)

with col1:
    nums_vao_sair = st.multiselect("Números que você acredita que vão sair:", options=list(range(1,26)))

with col2:
    nums_nao_sair = st.multiselect("Números que você acredita que NÃO vão sair:", options=list(range(1,26)))

# Validação para não permitir que um número esteja nos dois grupos
if set(nums_vao_sair).intersection(set(nums_nao_sair)):
    st.error("Erro: um número não pode estar tanto em 'vai sair' quanto em 'não vai sair'. Corrija a seleção.")
else:
    st.subheader("Sugestões com base nas suas escolhas")

    # Frequência dos números nos últimos sorteios escolhidos
    todos_numeros = ultimos_sorteios.iloc[:, 2:].values.flatten()
    freq = pd.Series(todos_numeros).value_counts().sort_index()

    df_freq = pd.DataFrame({
        'Número': range(1, 26),
        'Frequência': [freq.get(num, 0) for num in range(1, 26)]
    })

    # Aplicar filtros do usuário
    if nums_vao_sair:
        df_freq.loc[~df_freq['Número'].isin(nums_vao_sair), 'Frequência'] = 0
    if nums_nao_sair:
        df_freq.loc[df_freq['Número'].isin(nums_nao_sair), 'Frequência'] = 0

    df_freq = df_freq.sort_values(by='Frequência', ascending=False).reset_index(drop=True)

    st.write("Frequência ajustada dos números (filtrada):")
    st.dataframe(df_freq)

    sugestao = df_freq[df_freq['Frequência'] > 0]['Número'].tolist()
    if len(sugestao) >= 15:
        sugestao = sugestao[:15]
        st.success(f"Sugestão de 15 números baseados nas suas escolhas: {sugestao}")
    else:
        st.warning("Não há números suficientes após aplicar os filtros. Ajuste suas escolhas.")

# Análise visual de repetição geral
st.subheader("Números que mais se repetem entre os últimos sorteios selecionados")
repetidos_geral = pd.Series(ultimos_sorteios.iloc[:, 2:].values.flatten()).value_counts()
st.bar_chart(repetidos_geral)
