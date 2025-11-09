import requests
import pandas as pd
import io

def baixar_resultados_asloterias(url: str) -> pd.DataFrame:
    """Baixa arquivo Excel/CSV da As Loterias com resultados da Lotofácil."""
    resp = requests.get(url)
    resp.raise_for_status()
    content = resp.content

    # Tentar abrir como Excel
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception:
        # fallback para CSV
        try:
            df = pd.read_csv(io.StringIO(content.decode('utf-8')), sep=';', engine='python')
        except Exception as e:
            raise ValueError(f"Não foi possível ler o arquivo baixado: {e}")

    # Conferir colunas mínimas
    if 'Concurso' not in df.columns or 'Data' not in df.columns:
        raise ValueError("Arquivo baixado não contém colunas 'Concurso' e 'Data'.")

    # Converter data
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.date

    return df

def carregar_dados_reais():
    # Substitua por link direto do arquivo Excel da As Loterias
    url = "COLE_AQUI_O_LINK_DIRETO_DO_XLSX"
    return baixar_resultados_asloterias(url)
