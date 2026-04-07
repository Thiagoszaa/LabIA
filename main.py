import pandas as pd
import numpy as np

# Carregando o dataset
df = pd.read_excel('dataset_sujo_restaurante.xlsx')

# Garantir padrão nas colunas
df.columns = df.columns.str.strip().str.lower()

# 1. Limpeza de nomes
df['nome_cliente'] = df['nome_cliente'].astype(str).str.strip().str.title()
df['nome_cliente'] = df['nome_cliente'].replace(['None', 'Nan'], 'Usuário Não Identificado')

# 2. Tratamento de idade (outliers e nulos)
mediana_idade = df[(df['idade'] > 0) & (df['idade'] < 120)]['idade'].median()

df['idade'] = df['idade'].apply(
    lambda x: mediana_idade if pd.isna(x) or x <= 0 or x > 120 else x
)

# 3. Padronização de cidade
df['cidade'] = df['cidade'].astype(str).str.strip().str.title()
df['cidade'] = df['cidade'].replace(['None', 'Nan'], 'Não Informado')

# 4. Padronização de status
status_map = {
    'entregue': 'Entregue',
    'pendente': 'Pendente',
    'cancelado': 'Cancelado'
}

df['status'] = df['status'].astype(str).str.strip().str.lower()
df['status'] = df['status'].map(status_map).fillna('Indefinido')

# 5. Tratamento de valor_pedido (outliers)
df['valor_pedido'] = pd.to_numeric(df['valor_pedido'], errors='coerce')

limite_outlier = df['valor_pedido'].mean() + (2 * df['valor_pedido'].std())

df['valor_pedido'] = df['valor_pedido'].apply(
    lambda x: df['valor_pedido'].median() if pd.isna(x) or x < 0 or x > limite_outlier else x
)

# 6. Tratamento de datas
df['data_pedido'] = pd.to_datetime(df['data_pedido'], errors='coerce')
df['data_pedido'] = df['data_pedido'].fillna(method='ffill')

# 7. Salvar dataset limpo
df.to_excel('dataset_limpo_restaurante.xlsx', index=False)

print("Dataset limpo gerado com sucesso!")