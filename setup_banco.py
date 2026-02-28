import sqlite3
import os

# 1. Garante que a pasta 'database' existe
os.makedirs('database', exist_ok=True)

# 2. Conecta ao banco DENTRO da pasta (se não existir, ele cria um novo)
conn = sqlite3.connect('database/frota.db')
cursor = conn.cursor()

# 3. Zera qualquer tabela quebrada que tenha ficado lá
cursor.execute("DROP TABLE IF EXISTS INVENTARIO")
cursor.execute("DROP TABLE IF EXISTS MANUTENCOES")

# 4. Cria a tabela INVENTARIO perfeita
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
print("✅ Tabela INVENTARIO recriada.")

# 5. Cria a tabela MANUTENCOES perfeita
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
print("✅ Tabela MANUTENCOES recriada.")

conn.commit()
conn.close()
print("🚀 SUCESSO! Banco de dados estruturado corretamente na pasta 'database'.")