import requests
import pandas as pd
import io

def baixar_resultados_asloterias(url: str) -> pd.DataFrame:
    """Baixa arquivo Excel/CSV da As Loterias com resultados da Lotofácil."""
    resp = requests.get(url)
    resp.raise_for_status()
    content = resp.content
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception:
        df = pd.read_csv(io.StringIO(content.decode('utf‑8')))
    if 'Concurso' not in df.columns or 'Data' not in df.columns:
        raise ValueError("Arquivo baixado não contém colunas 'Concurso' e 'Data'.")
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.date
    return df

def carregar_dados_reais():
    url = "https://asloterias.com.br/download-todos-resultados-lotofacil"  # Página de download da planilha. Substitua por link direto se achar.
    return baixar_resultados_asloterias(url)
