import streamlit as st
import pandas as pd
import numpy as np

# Exemplo de dados: aqui você deve colocar a função para baixar/ler os dados reais da Lotofácil
# Vou simular dados para ilustrar:
def carregar_dados():
    # Simula resultados históricos: cada linha um sorteio, 15 números sorteados de 1 a 25
    np.random.seed(42)
    sorteios = []
    for i in range(100):  # 100 sorteios simulados
        sorteios.append(sorted(np.random.choice(range(1,26), 15, replace=False)))
    df = pd.DataFrame(sorteios, columns=[f'Num{i+1}' for i in range(15)])
    return df

df = carregar_dados()

st.title("Análise Avançada da Lotofácil")

# Seleção do número de sorteios para análise
num_sorteios = st.slider("Quantos últimos sorteios considerar para análise?", min_value=2, max_value=len(df), value=10)

# Dados filtrados
ultimos_sorteios = df.tail(num_sorteios).reset_index(drop=True)

st.subheader(f"Últimos {num_sorteios} sorteios")
st.dataframe(ultimos_sorteios)

# Botão para números repetidos do último sorteio para o anterior
if st.button("Mostrar números repetidos entre os 2 últimos sorteios"):
    if len(ultimos_sorteios) < 2:
        st.warning("Escolha pelo menos 2 sorteios para essa análise.")
    else:
        ultimo = set(ultimos_sorteios.iloc[-1])
        penultimo = set(ultimos_sorteios.iloc[-2])
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
    # Análise básica de probabilidade com filtros
    st.subheader("Sugestões com base nas suas escolhas")

    # Frequência dos números nos últimos sorteios escolhidos
    todos_numeros = ultimos_sorteios.values.flatten()
    freq = pd.Series(todos_numeros).value_counts().sort_index()

    # Criar DataFrame para facilitar visualização
    df_freq = pd.DataFrame({
        'Número': range(1,26),
        'Frequência': [freq.get(num, 0) for num in range(1,26)]
    })

    # Aplicar filtros de preferências do usuário
    if nums_vao_sair:
        # Força a incluir pelo menos esses números
        df_freq.loc[~df_freq['Número'].isin(nums_vao_sair), 'Frequência'] = 0

    if nums_nao_sair:
        # Remove esses números
        df_freq.loc[df_freq['Número'].isin(nums_nao_sair), 'Frequência'] = 0

    # Ordena pelo maior valor
    df_freq = df_freq.sort_values(by='Frequência', ascending=False).reset_index(drop=True)

    st.write("Frequência ajustada dos números nos últimos sorteios (filtrada):")
    st.dataframe(df_freq)

    # Sugestão de 15 números com maior frequência depois do filtro
    sugestao = df_freq[df_freq['Frequência'] > 0]['Número'].tolist()
    if len(sugestao) >= 15:
        sugestao = sugestao[:15]
        st.success(f"Sugestão de 15 números baseados nas suas escolhas: {sugestao}")
    else:
        st.warning("Não há números suficientes após aplicar os filtros. Tente ajustar suas escolhas.")

# Extras - análise de repetição geral entre os últimos N sorteios
st.subheader("Números que mais se repetem entre os últimos sorteios selecionados")
repetidos_geral = pd.Series(ultimos_sorteios.values.flatten()).value_counts()
st.bar_chart(repetidos_geral)

