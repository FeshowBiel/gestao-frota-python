import sqlite3

# Conecta ao banco existente
conn = sqlite3.connect('database/frota.db')
cursor = conn.cursor()

try:
    # Adiciona a coluna 'status' e já define que todos os veículos atuais estão 'Ativos'
    cursor.execute("ALTER TABLE INVENTARIO ADD COLUMN status TEXT DEFAULT 'Ativo'")
    conn.commit()
    print("✅ Coluna 'status' adicionada com sucesso ao banco de dados!")
except sqlite3.OperationalError:
    print("⚠️ A coluna 'status' já existe no banco de dados.")

conn.close()