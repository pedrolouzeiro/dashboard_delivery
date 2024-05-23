from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import datetime
import utils
import pandas as pd

df_original = pd.read_csv('dataset/train.csv')
df = utils.clean_code(df_original)


import streamlit as st

st.set_page_config(page_title='Marketplace - Visão Entregadores',  layout='wide',initial_sidebar_state="collapsed")
#=======================
#Barra Lateral
#=======================
st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    ' ',
    value=datetime.datetime(2022,3,11),
    min_value=datetime.datetime(2022,2,11),
    max_value=datetime.datetime(2022,4,6),
    format='DD-MM-YYYY'
)
st.sidebar.markdown("""---""")

traffic_options=st.sidebar.multiselect(
    'Condições de Trânsito',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam']
)
st.sidebar.markdown("""---""")

clima_options=st.sidebar.multiselect(
    'Condições do Clima',
    ['Cloudy','Fog','Sandstorms','Stormy','Sunny','Windy'],
    default=['Cloudy','Fog','Sandstorms','Stormy','Sunny','Windy']
)

st.sidebar.markdown("""---""")

city_options = st.sidebar.multiselect(
    'Cidade',
    ['Semi-Urban','Urban','Metropolitian'],
    default=['Semi-Urban']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown('## Feito por Pedro Louzeiro')

#Filtro data
linhas_selecionadas = df['Order_Date'] <= date_slider
df = df.loc[linhas_selecionadas]

#Filtro de trânsito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas]

#Filtro de clima
linhas_selecionadas = df['Weatherconditions'].isin(clima_options)
df = df.loc[linhas_selecionadas]

#Filtro de cidade
linhas_selecionadas = df['City'].isin(city_options)
df = df.loc[linhas_selecionadas]
#st.dataframe(df)


#=======================
#Layout
#=======================
tab1, tab2 = st.tabs(['Visão Gerencial',' '])



with tab1:
    with st.container():

        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:

            maior_idade=df['Delivery_person_Age'].max()
            col1.metric('Maior Idade', maior_idade)
        with col2:

            menor_idade=df['Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
           
        with col3:

            melhor_condicao=df['Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_condicao)
            
        with col4:

            pior_condicao=df['Vehicle_condition'].min()
            col4.metric('Pior Condição', pior_condicao)
            
    with st.container():

        st.title('Avaliações')
        
        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Avaliação Média por Entregador')
            avg_por_entregador=df.groupby(['Delivery_person_ID'])['Delivery_person_Ratings'].mean().reset_index()
            st.dataframe(avg_por_entregador)
            
        with col2:
            
            st.markdown('##### Avaliação Média e Desvio Padrão por Trânsito')
            ag=df.groupby(['Road_traffic_density'])['Delivery_person_Ratings'].agg(['mean', 'std'])
            ag.columns = ['d_mean','d_std']
            avg_por_transito=ag.reset_index()
            st.dataframe(avg_por_transito)
            
            st.markdown('##### Avaliação Média e Desvio Padrão por Clima')
            avg_por_clima=df.groupby(['Weatherconditions'])['Delivery_person_Ratings'].agg(['mean', 'std']).reset_index()
            st.dataframe(avg_por_clima)
            
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            tp = utils.top(df, ordem=True)
            st.markdown('##### Entregadores mais rápidos') 
            st.dataframe(tp)
            
        with col2:
            tp = utils.top(df, ordem=False)
            st.markdown('##### Entregadores mais lentos')
            st.dataframe(tp)
            