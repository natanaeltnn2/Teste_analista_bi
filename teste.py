import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

def extrair_dados():
    file_path = '69021137a36083d14124e274-1f3676c4-9e7e-4931-a558-ff7a0079e8bb.xlsx'

    df_sheet1 = pd.read_excel(file_path, sheet_name='Vendas')
    #.replace('-','/')
    s = pd.to_datetime(df_sheet1['Data_Pedido'])

    # Converter para mês/ano e virar lista
    lista_mes_ano = s.dt.strftime("%m/%Y").tolist()
    #print(lista_mes_ano)
    df_sheet1['Mês/Ano da Venda'] = lista_mes_ano
    df_sheet2 = pd.read_excel(file_path, sheet_name='Produtos')
    df_sheet2['Lucro por item'] = df_sheet2['Preco_Venda'] - df_sheet2['Custo_Unitario']
    df_sheet2['Margem (%)'] = df_sheet2['Lucro por item']/df_sheet2['Preco_Venda']
    df_sheet3 = pd.read_excel(file_path, sheet_name='Unidades')

    Vendas_Produtos_df = pd.merge(df_sheet1, df_sheet2, on='Produto_ID', how='inner')
    #Vendas_Unidades_df = pd.merge(df_sheet1, df_sheet3, on='Unidade_ID', how='inner')

    Vendas_Produtos_df = pd.merge(Vendas_Produtos_df, df_sheet3, on='Unidade_ID', how='inner')
    return Vendas_Produtos_df

def show_graf(Vendas_Produtos_df):
    # Calcula total e média por mês/ano
    df_grouped = Vendas_Produtos_df.groupby("Unidade_ID", as_index=False).agg(
        Total_de_Faturamento=("Valor_Total", "sum"),
        Media_de_Faturamento=('Margem (%)', "mean")
    )

    # Gráfico de barras (totais por mês)
    bars = alt.Chart(df_grouped).mark_bar().encode(
        x="Unidade_ID:N",
        y="Total_de_Faturamento:Q",
        tooltip=[
            "Unidade_ID",
            "Total_de_Faturamento",
            "Media_de_Faturamento"
        ]
    )

    # Linha conectando as médias por mês
    line = alt.Chart(df_grouped).mark_line(
        color="red",
        strokeWidth=2
    ).encode(
        x="Unidade_ID:N",
        y="Media_de_Faturamento:Q"
    )

    # Pontos nas médias (opcional)
    points = alt.Chart(df_grouped).mark_point(
        color="red",
        size=70
    ).encode(
        x="Unidade_ID:N",
        y="Media_de_Faturamento:Q"
    )

    # Label acima do ponto da média
    labels = alt.Chart(df_grouped).mark_text(
        align="center",
        dy=-10,
        fontSize=12,
        fontWeight="bold",
        color="black"
    ).encode(
        x="Unidade_ID:N",
        y="Media_de_Faturamento:Q",
        text=alt.Text("Media_de_Faturamento:Q", format=".2f")
    )

    chart = (bars + line + points + labels).properties(
        width=650,
        height=400,
        title="Total vs Média de Faturamento por Mês/Ano"
    )

    st.altair_chart(chart, use_container_width=True)

def acompanhamento_ao_decorrer_meses(df):
    df_grouped = Vendas_Produtos_df.groupby('Mês/Ano da Venda', as_index=False).agg(
        Total_de_Faturamento=("Valor_Total", "sum"),
    )

    #print(df_grouped)
    # Gráfico de linhas
    chart = (
        alt.Chart(df_grouped)
        .mark_line(point=True)  # point=True adiciona marcadores
        .encode(
            x=alt.X("Mês/Ano da Venda:N", title="Mês/Ano da Venda"),
            y=alt.Y("Total_de_Faturamento:Q", title="Faturamento (R$)"),
            tooltip=["Mês/Ano da Venda", "Total_de_Faturamento"]
        )
    )

    st.altair_chart(chart, use_container_width=True)

def garcons_pedidos(Vendas_Produtos_df):
    # Gráfico horizontal
    chart = (
        alt.Chart(Vendas_Produtos_df)
        .mark_bar()
        .encode(
            x=alt.X("Quantidade:Q", title="Volume de vendas"),
            y=alt.Y("Garcom:N", sort="-x", title="Garçom"),  # sort -x = ordenar do maior para o menor
            tooltip=["Garcom", "Quantidade"]
        )
    )

    st.altair_chart(chart, use_container_width=True)

def graf_categorias(df):
    # Calcula total e média por mês/ano
    df_grouped = Vendas_Produtos_df.groupby("Categoria", as_index=False).agg(
        Total_de_Faturamento=("Valor_Total", "sum"),
        Media_de_Faturamento=('Margem (%)', "mean")
    )

    # Gráfico de barras (totais por mês)
    bars = alt.Chart(df_grouped).mark_bar().encode(
        x="Categoria:N",
        y="Total_de_Faturamento:Q",
        tooltip=[
            "Categoria",
            "Total_de_Faturamento",
            "Media_de_Faturamento"
        ]
    )

    # Linha conectando as médias por mês
    line = alt.Chart(df_grouped).mark_line(
        color="red",
        strokeWidth=2
    ).encode(
        x="Categoria:N",
        y="Media_de_Faturamento:Q"
    )

    # Pontos nas médias (opcional)
    points = alt.Chart(df_grouped).mark_point(
        color="red",
        size=70
    ).encode(
        x="Categoria:N",
        y="Media_de_Faturamento:Q"
    )

    # Label acima do ponto da média
    labels = alt.Chart(df_grouped).mark_text(
        align="center",
        dy=-10,
        fontSize=12,
        fontWeight="bold",
        color="black"
    ).encode(
        x="Categoria:N",
        y="Media_de_Faturamento:Q",
        text=alt.Text("Media_de_Faturamento:Q", format=".2f")
    )

    chart = (bars + line + points + labels).properties(
        width=650,
        height=400,
        title="Total vs Média de Faturamento por Mês/Ano"
    )

    st.altair_chart(chart, use_container_width=True)

def acompanhamento_ao_decorrer_meses(df):
    df_grouped = Vendas_Produtos_df.groupby('Mês/Ano da Venda', as_index=False).agg(
        Total_de_Faturamento=("Valor_Total", "sum"),
    )

    # Gráfico de linhas
    chart = (
        alt.Chart(df_grouped)
        .mark_line(point=True)  # point=True adiciona marcadores
        .encode(
            x=alt.X("Mês/Ano da Venda:N", title="Mês/Ano da Venda"),
            y=alt.Y("Total_de_Faturamento:Q", title="Faturamento (R$)"),
            tooltip=["Mês/Ano da Venda", "Total_de_Faturamento"]
        )
    )

    st.altair_chart(chart, use_container_width=True)

import json
import urllib

def graf_brazil(df):
    df_grouped = (
    df.groupby(["Cidade", "Estado", "Gerente"], as_index=False)
      .size()
      .rename(columns={"size": "Numero_de_Pedidos"})
)
    st.table(df_grouped)

Vendas_Produtos_df2 = extrair_dados()
print(Vendas_Produtos_df2.values.shape)
#1/0
unique_months = Vendas_Produtos_df2['Mês/Ano da Venda'].unique()
unique_categorias = Vendas_Produtos_df2['Categoria'].unique()


selected_rows = st.multiselect(
    "Selecione um ou mais meses:",
    unique_months
)

selected_rows_cat = st.multiselect(
    "Selecione uma ou mais categorias:",
    unique_categorias
)

Vendas_Produtos_df = Vendas_Produtos_df2

print(selected_rows)
if selected_rows:
    Vendas_Produtos_df = Vendas_Produtos_df[Vendas_Produtos_df['Mês/Ano da Venda'].isin(selected_rows)]
if selected_rows_cat:
    Vendas_Produtos_df = Vendas_Produtos_df[Vendas_Produtos_df['Categoria'].isin(selected_rows_cat)]
    print(Vendas_Produtos_df)

    #Vendas_Unidades_df = Vendas_Unidades_df2[Vendas_Unidades_df2['Categoria'].isin(selected_rows)]

# Total de faturamento geral
total_faturamento = Vendas_Produtos_df["Valor_Total"].sum()

margem_total = 100*(Vendas_Produtos_df['Lucro por item']*Vendas_Produtos_df['Quantidade']).sum()/total_faturamento

col1, col2 = st.columns(2)
with col1:
    st.metric(
            label="💰 Faturamento Total",
            value=f"R$ {total_faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

with col2:
    st.metric(
            label="📈 Margem de Lucro",
            value=f"{margem_total:.2f} %"
        )
    
acompanhamento_ao_decorrer_meses(Vendas_Produtos_df)
show_graf(Vendas_Produtos_df)

col3, col4 = st.columns([0.6,0.4])

with col3:
    #novo = Vendas_Produtos_df,Vendas_Unidades_df
    graf_brazil(Vendas_Produtos_df)
    graf_categorias(Vendas_Produtos_df)
with col4:
    
    garcons_pedidos(Vendas_Produtos_df)