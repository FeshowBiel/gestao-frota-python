import sqlite3
import pandas as pd

def criar_banco_do_zero():
    # Nome do arquivo que será criado
    nome_banco = 'frota.db'
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    print("🛠️ Criando tabelas...")

    # 1. Criar Tabela de INVENTÁRIO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS INVENTARIO (
            placa TEXT,
            marca TEXT,
            modelo TEXT,
            ano INTEGER,
            status TEXT
        )
    ''')

    # 2. Criar Tabela de MANUTENCAO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS [Manutenção Preventiva] (
            placa TEXT,
            data TEXT,
            valor REAL,
            fornecedor TEXT,
            status TEXT
        )
    ''')

    print("📝 Inserindo dados de exemplo...")

    # Dados de Exemplo para Inventário
    veiculos = [
        ('ABC1234', 'VOLVO', 'FH 540', 2022, 'Ativo'),
        ('XYZ5678', 'SCANIA', 'R450', 2021, 'Manutenção'),
        ('GAB2026', 'MERCEDES', 'ACTROS', 2023, 'Ativo')
    ]
    cursor.executemany('INSERT INTO INVENTARIO VALUES (?,?,?,?,?)', veiculos)

    # Dados de Exemplo para Manutenção (Janeiro/Fevereiro 2026)
    manutencoes = [
        ('ABC1234', '2026-01-15', 1250.00, 'Oficina do João', 'OK'),
        ('XYZ5678', '2026-02-20', 850.00, 'Auto Elétrica Diesel', 'Pendente'),
        ('GAB2026', '2026-03-01', 0.00, 'Borracharia Central', 'Agendado')
    ]
    cursor.executemany('[Manutenção Preventiva] VALUES (?,?,?,?,?)', manutencoes)

    conn.commit()
    conn.close()
    print(f"🚀 Sucesso! O arquivo '{nome_banco}' foi criado com exemplos.")

if __name__ == "__main__":
    criar_banco_do_zero()