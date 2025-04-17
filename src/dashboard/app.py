# import
import streamlit as st
import pandas as pd
import sqlite3
from pyngrok import ngrok

# Função para listar as tabelas disponíveis no banco
def get_table_names(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    return tables

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('data/mercadolivre.db')

# Obter nomes das tabelas
table_names = get_table_names(conn)

# Interface para selecionar tabela
st.sidebar.title("🔍 Selecione um produto")
selected_table = st.sidebar.selectbox("Tabelas disponíveis:", table_names)

# Carregar os dados da tabela selecionada
df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)

# Fechar conexão
conn.close()

# Título da aplicação
st.title(f'📊 Pesquisa de Mercado - {selected_table.capitalize()} no Mercado Livre')

# KPIs
st.subheader('💡 KPIs principais')
col1, col2, col3 = st.columns(3)
col1.metric("📦 Total de Itens", df.shape[0])
col2.metric("🏷️ Marcas Únicas", df['brand'].nunique())
col3.metric("💰 Preço Médio (R$)", f"{df['new_money'].mean():.2f}")

# Marcas mais frequentes
st.subheader('🏆 Marcas mais encontradas até a 10ª página')
col1, col2 = st.columns([4, 2])
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

# Preço médio por marca
st.subheader('💵 Preço médio por marca')
col1, col2 = st.columns([4, 2])
df_non_zero_prices = df[df['new_money'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_money'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# Satisfação média por marca
st.subheader('⭐ Satisfação média por marca')
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)

# Abre el túnel para el puerto 8501, que es el default de Streamlit
public_url = ngrok.connect(8501)
print("🌍 URL pública de Streamlit:", public_url)