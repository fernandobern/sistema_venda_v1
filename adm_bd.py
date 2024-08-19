import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('sistema_vendas.db')

# Adicionar colunas à tabela de vendas

conn.execute('''
ALTER TABLE vendas
ADD COLUMN valor_total real;
''')

# Commit da alteração
conn.commit()

# Fechar a conexão
conn.close()
