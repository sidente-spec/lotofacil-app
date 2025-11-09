import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def carregar_dados():
    """Simula a carga de dados históricos da Lotofácil."""
    np.random.seed(42)
    sorteios = []
    datas = []
    base_date = datetime.today() - timedelta(days=100*3)
    for i in range(100):
        numeros = sorted(np.random.choice(range(1, 26), 15, replace=False))
        sorteios.append(numeros)
        datas.append(base_date + timedelta(days=i*3))
    df = pd.DataFrame(sorteios, columns=[f'Num{i+1}' for i in range(15)])
    df['Concurso'] = range(1, 101)
    df['Data'] = pd.to_datetime(datas).dt.date
    colunas = ['Concurso', 'Data'] + [f'Num{i+1}' for i in range(15)]
    df = df[colunas]
    return df

def atualizar_jogos():
    """Função para atualizar/baixar dados reais. Aqui ainda simula."""
    return carregar_dados()
