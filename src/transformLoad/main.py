import pandas as pd
import sqlite3
from datetime import datetime

# Definir o caminho para o arquivo JSONL
df = pd.read_json('data/products/ofertas_dia.jsonl', lines=True)

# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar a coluna _source com um valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/ofertas"

# Adicionar a coluna _datetime com a data e hora atuais
df['_datetime'] = datetime.now()

# Tratar nulos
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('(0)')

# Garantir que estão como strings antes de usar .str
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex=False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace('[\(\)]', '', regex=True)

# Converter para números
df['old_money'] = df['old_money'].astype(float)
df['new_money'] = df['new_money'].astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].astype(float)
df['reviews_amount'] = df['reviews_amount'].astype(int)

# Manter apenas produtos com preço entre 1000 e 10000 reais
df = df[
    (df['old_money'] >= 1000) & (df['old_money'] <= 10000) &
    (df['new_money'] >= 1000) & (df['new_money'] <= 10000)
]

# Dividir a coluna category_path em colunas separadas
if 'category_path' in df.columns:
    category_cols = df['category_path'].str.split(' > ', expand=True)
    category_cols.columns = [f'category_level_{i+1}' for i in range(category_cols.shape[1])]
    df = pd.concat([df, category_cols], axis=1)

df['category_path'] = df['category_path'].drop

# Conectar ao banco de dados SQLite (ou criar um novo)
conn = sqlite3.connect('data/mercadolivreOfertas.db')

# Salvar o DataFrame no banco de dados SQLite
df.to_sql('ofertasDia', conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()
#print(df)