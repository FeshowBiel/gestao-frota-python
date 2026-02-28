import sqlite3
import pandas as pd

# Agora apontando para a pasta correta!
DB_PATH = 'database/frota.db'

def executar_query(sql, dados=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if dados:
        cursor.execute(sql, dados)
    else:
        cursor.execute(sql)
    conn.commit()
    conn.close()

def carregar_dados(tabela):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM [{tabela}]", conn)
    conn.close()
    return df