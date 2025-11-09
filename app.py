import streamlit as st
import pandas as pd
from lotofacil_utils import carregar_dados_reais

st.set_page_config(page_title="Estatísticas Lotofácil", layout="wide")

st.title("📊 Estatísticas da Lotofácil")

if 'df_lotofacil' not in st.session_state:
    try:
        st.session_state.df_lotofacil = carregar_dados_reais()
    except Exception as e:
        st.error(f"Erro ao carregar dados reais: {e}")
        st.stop()

if st.button("🔄 Atualizar jogos (baixar últimos resultados)"):
    try:
        st.session_state.df_lotofacil = carregar_dados_reais()
        st.success("Jogos atualizados com dados reais!")
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")

df = st.session_state.df_lotofacil

# Mostrar tabela completa
st.subheader("📅 Últimos resultados")
st.dataframe(df)

# Seletor de quantidade de sorteios para análise
num_sorteios = st.slider("Quantos últimos sorteios considerar?", min_value=2, max_value=len(df), value=10)
ultimos = df.tail(num_sorteios).reset_index(drop=True)

st.subheader(f"Últimos {num_sorteios} sorteios")
st.dataframe(ultimos)

# Botão para repetidos entre 2 últimos sorteios
if st.button("Mostrar números repetidos entre os 2 últimos sorteios"):
    if len(ultimos) < 2:
        st.warning("Escolha pelo menos 2 sorteios.")
    else:
        conjunto1 = set(ultimos.iloc[-1].drop(['Concurso','Data']))
        conjunto2 = set(ultimos.iloc[-2].drop(['Concurso','Data']))
        repetidos = sorted(conjunto1.intersection(conjunto2))
        st.write(f"Números repetidos: {repetidos if repetidos else 'Nenhum número repetido'}")

# Seleção de números que vão e que não vão sair
st.subheader("Escolha seus números de confiança")
col1, col2 = st.columns(2)
with col1:
    nums_vao = st.multiselect("Números que você acredita que vão sair:", options=list(range(1,26)))
with col2:
    nums_nao = st.multiselect("Números que você acredita que NÃO vão sair:", options=list(range(1,26)))

if set(nums_vao).intersection(set(nums_nao)):
    st.error("Erro: um número não pode estar em ambos os grupos.")
else:
    st.subheader("🔮 Sugestões baseadas nas suas escolhas")
    # Frequência considerando últimos sorteios
    apenas_numeros = ultimos.drop(['Concurso','Data'], axis=1).values.flatten()
    freq = pd.Series(apenas_numeros).value_counts().sort_index()
    df_freq = pd.DataFrame({
        'Número': range(1,26),
        'Frequência': [freq.get(num,0) for num in range(1,26)]
    })
    if nums_vao:
        df_freq.loc[~df_freq['Número'].isin(nums_vao), 'Frequência'] = 0
    if nums_nao:
        df_freq.loc[df_freq['Número'].isin(nums_nao), 'Frequência'] = 0
    df_freq = df_freq.sort_values(by='Frequência', ascending=False).reset_index(drop=True)
    st.write("Frequência ajustada:")
    st.dataframe(df_freq)
    sugestao = df_freq[df_freq['Frequência']>0]['Número'].tolist()
    if len(sugestao) >= 15:
        sugestao = sugestao[:15]
        st.success(f"Sugestão de 15 números: {sugestao}")
    else:
        st.warning("Não há números suficientes após aplicar os filtros.")

# Gráfico de repetição geral
st.subheader("Números que mais se repetem entre os últimos sorteios selecionados")
repetidos_geral = pd.Series(ultimos.drop(['Concurso','Data'], axis=1).values.flatten()).value_counts()
st.bar_chart(repetidos_geral)
