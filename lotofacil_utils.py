import requests
import pandas as pd
import io

def baixar_resultados_asloterias(url: str) -> pd.DataFrame:
    """
    Baixa arquivo Excel/CSV da As Loterias com resultados da Lotofácil.
    Retorna um DataFrame com colunas: Concurso, Data, Num1, ..., Num15
    """
    resp = requests.get(url)
    resp.raise_for_status()
    content = resp.content

    # Tentar abrir como Excel primeiro
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception:
        # fallback para CSV
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))

    # Verificar se contém colunas essenciais
    if 'Concurso' not in df.columns or 'Data' not in df.columns:
        raise ValueError("Arquivo baixado não contém colunas 'Concurso' e 'Data'.")

    # Converter coluna Data para datetime.date
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.date

    return df

def carregar_dados_reais():
    """
    Função principal para carregar os resultados da Lotofácil.
    Substitua o link abaixo pelo link direto da planilha da As Loterias.
    """
    url = "COLE_AQUI_LINK_EXATO_DA_PLANILHA"  # <-- cole o link direto aqui
    return baixar_resultados_asloterias(url)
