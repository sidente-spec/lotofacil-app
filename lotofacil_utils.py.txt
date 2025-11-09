import requests
import pandas as pd
import random

URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil"

def baixar_resultado_atual():
    """Baixa o último resultado da Lotofácil da API da Caixa."""
    headers = {"accept": "application/json"}
    response = requests.get(URL, headers=headers)
    data = response.json()

    dezenas = [int(n) for n in data["listaDezenas"]]
    concurso = int(data["numero"])
    data_sorteio = data["dataApuracao"]

    df = pd.DataFrame([{
        "concurso": concurso,
        "data": data_sorteio,
        **{f"dezena_{i+1}": dezenas[i] for i in range(15)}
    }])

    return df

def atualizar_resultados(caminho_csv="resultados.csv"):
    """Atualiza o histórico de resultados, adicionando novos concursos."""
    try:
        df_existente = pd.read_csv(caminho_csv)
        ultimo_concurso = df_existente["concurso"].max()
    except FileNotFoundError:
        df_existente = pd.DataFrame()
        ultimo_concurso = 0

    novo = baixar_resultado_atual()
    if novo["concurso"].iloc[0] > ultimo_concurso:
        df_atualizado = pd.concat([df_existente, novo], ignore_index=True)
        df_atualizado.to_csv(caminho_csv, index=False)
        return df_atualizado, True
    else:
        return df_existente, False

def calcular_estatisticas(df):
    """Calcula estatísticas básicas das dezenas."""
    dezenas = df.filter(like="dezena_").values.flatten()
    freq = pd.Series(dezenas).value_counts().sort_index()

    stats = pd.DataFrame({
        "Dezena": freq.index,
        "Frequência": freq.values,
        "Probabilidade (%)": (freq.values / freq.sum()) * 100
    }).sort_values(by="Dezena")

    return stats

def sugerir_dezenas(stats, qtd=15):
    """Sugere dezenas com base nas mais frequentes."""
    top = stats.sort_values(by="Frequência", ascending=False).head(qtd)["Dezena"].tolist()
    return sorted(random.sample(top, 15))
