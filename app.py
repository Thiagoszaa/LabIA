import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Restaurante", layout="wide")

# Função para carregar os dados
@st.cache_data
def load_data():
    df = pd.read_excel('dataset_limpo_restaurante.xlsx')
    
    # Padronizar colunas
    df.columns = df.columns.str.strip().str.lower()
    
    # Converter data
    df['data_pedido'] = pd.to_datetime(df['data_pedido'])
    
    return df

try:
    df = load_data()

    # ===== TÍTULO =====
    st.title("📊 Dashboard de Operações - Restaurante")

    # ===== FILTROS =====
    st.sidebar.header("🔎 Filtros")

    cidades = st.sidebar.multiselect(
        "Cidade",
        options=df['cidade'].unique(),
        default=df['cidade'].unique()
    )

    status = st.sidebar.multiselect(
        "Status",
        options=df['status'].unique(),
        default=df['status'].unique()
    )

    df_filtrado = df[
        (df['cidade'].isin(cidades)) &
        (df['status'].isin(status))
    ]

    # ===== MÉTRICAS =====
    st.subheader("📈 Indicadores")

    m1, m2, m3 = st.columns(3)

    m1.metric("💰 Faturamento Total", f"R$ {df_filtrado['valor_pedido'].sum():,.2f}")
    m2.metric("📦 Total de Pedidos", df_filtrado.shape[0])
    m3.metric("📊 Ticket Médio", f"R$ {df_filtrado['valor_pedido'].mean():,.2f}")

    st.divider()

    # ===== GRÁFICOS =====
    col1, col2 = st.columns(2)

    # Pizza - Status
    with col1:
        st.subheader("📦 Status dos Pedidos")
        fig_status = px.pie(df_filtrado, names='status')
        st.plotly_chart(fig_status, use_container_width=True)

    # Barras - Cidade
    with col2:
        st.subheader("🏙️ Pedidos por Cidade")
        cidades_df = df_filtrado['cidade'].value_counts().reset_index()
        cidades_df.columns = ['cidade', 'quantidade']
        fig_cidade = px.bar(cidades_df, x='cidade', y='quantidade', color='cidade')
        st.plotly_chart(fig_cidade, use_container_width=True)

    # Linha - Evolução no tempo
    st.subheader("📅 Evolução de Faturamento")

    evolucao = df_filtrado.groupby('data_pedido')['valor_pedido'].sum().reset_index()

    fig_linha = px.line(
        evolucao,
        x='data_pedido',
        y='valor_pedido',
        markers=True
    )

    st.plotly_chart(fig_linha, use_container_width=True)

    # ===== TABELA =====
    st.subheader("📋 Dados")
    st.dataframe(df_filtrado)

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")