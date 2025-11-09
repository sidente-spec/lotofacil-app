import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lotofacil_utils import atualizar_resultados, calcular_estatisticas, sugerir_dezenas

st.set_page_config(page_title="📊 Lotofácil Stats Online", layout="wide")

st.title("🍀 Lotofácil Stats Online")
st.markdown("Acompanhe estatísticas e probabilidades atualizadas da Lotofácil (dados oficiais da Caixa).")

# Atualizar resultados
with st.spinner("🔄 Atualizando resultados..."):
    df, atualizado = atualizar_resultados()

if atualizado:
    st.success("✅ Novo sorteio encontrado e adicionado!")
else:
    st.info("ℹ️ Nenhum novo sorteio encontrado.")

st.subheader("📅 Últimos sorteios")
st.dataframe(df.tail(5), use_container_width=True)

# Estatísticas
st.subheader("📈 Frequência das Dezenas")
stats = calcular_estatisticas(df)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(stats["Dezena"], stats["Frequência"], color="#6C63FF")
ax.set_title("Frequência das dezenas mais sorteadas")
ax.set_xlabel("Dezena")
ax.set_ylabel("Número de vezes sorteada")
st.pyplot(fig)

st.subheader("📋 Estatísticas detalhadas")
st.dataframe(stats, use_container_width=True)

# Sugestão de dezenas
st.markdown("---")
st.subheader("🔮 Sugestão de dezenas mais prováveis")
qtd = st.slider("Quantas dezenas sugerir?", 15, 25, 15)
sugestoes = sugerir_dezenas(stats, qtd)
st.write("Baseado na frequência histórica dos sorteios:")
st.success(", ".join(map(str, sugestoes)))

st.markdown("---")
st.caption("Feito com ❤️ por ChatGPT | Dados: Caixa Econômica Federal")
