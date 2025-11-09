import requests
import pandas as pd
import io

def baixar_resultados_asloterias(url: str) -> pd.DataFrame:
    """Baixa arquivo Excel/CSV da As Loterias com resultados da Lotofácil."""
    resp = requests.get(url)
    resp.raise_for_status()
    content = resp.content
    try:
        # tentar Excel primeiro
        df = pd.read_excel(io.BytesIO(content))
    except Exception:
        # fallback para CSV
        df = pd.read_csv(io.StringIO(content.decode('utf‑8')))
    # Ajuste de colunas conforme experimento
    # Verificar se possui colunas 'Concurso' e 'Data'
    if 'Concurso' not in df.columns or 'Data' not in df.columns:
        raise ValueError("Arquivo baixado não contém colunas esperadas 'Concurso' e 'Data'.")
    # Converter Data para tipo date
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.date
    return df

def carregar_dados_reais():
    url = "COLE_AQUI_LINK_EXATO_DA_PLANILHA"
    return baixar_resultados_asloterias(url)
