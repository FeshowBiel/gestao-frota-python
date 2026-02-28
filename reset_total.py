import os
import sqlite3

# Define onde o banco está salvo (ajuste se estiver em outra pasta)
# Tentando adivinhar o padrão do seu projeto
caminho_db = "frota.db" 
if os.path.exists("database/frota.db"):
    caminho_db = "database/frota.db"
elif os.path.exists("db/frota.db"):
    caminho_db = "db/frota.db"

# 1. DELETA O ARQUIVO FÍSICO (A Solução Nuclear)
try:
    if os.path.exists(caminho_db):
        os.remove(caminho_db)
        print(f"🗑️ Arquivo fantasma '{caminho_db}' foi destruído com sucesso!")
except PermissionError:
    print(f"⚠️ ERRO: O arquivo '{caminho_db}' está aberto em outro programa. Feche tudo e tente de novo.")
    exit()

# 2. CRIA UM BANCO NOVO DO ZERO
conn = sqlite3.connect(caminho_db)
cursor = conn.cursor()

# Recria a tabela de Veículos
cursor.execute("""
CREATE TABLE INVENTARIO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    marca TEXT,
    modelo TEXT,
    ano INTEGER,
    km INTEGER
)
""")
print("✅ Tabela INVENTARIO criada.")

# Recria a tabela de Manutenções (COM A COLUNA PLACA)
cursor.execute("""
CREATE TABLE MANUTENCOES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    PLACA TEXT NOT NULL,
    DATA TEXT NOT NULL,
    DESCRICAO TEXT,
    TIPO TEXT,
    VALOR REAL
)
""")
print("✅ Tabela MANUTENCOES criada com todas as colunas perfeitas!")

conn.commit()
conn.close()
print("🚀 Tudo pronto! Pode voltar a rodar o Streamlit.")