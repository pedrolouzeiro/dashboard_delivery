from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd
import utils
import streamlit as st


df_original = pd.read_csv('dataset/train.csv')
df = utils.clean_code(df_original)

#Início Dashboard
st.set_page_config(page_title='Marketplace - Visão Empresa',  layout='wide', initial_sidebar_state="collapsed")

#=======================
#Barra Lateral
#=======================

#image_path = 'logo.png'
#image = Image.open(image_path)
#st.sidebar.image(image, width=120)

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
#st.dataframe(df)

#Filtro de clima
linhas_selecionadas = df['Weatherconditions'].isin(clima_options)
df = df.loc[linhas_selecionadas]
#Filtro de cidade
linhas_selecionadas = df['City'].isin(city_options)
df = df.loc[linhas_selecionadas]


#=======================
#Layout
#=======================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    with st.container():
        fig = utils.pedidos_por_dia(df)
        st.markdown('# Pedidos por Dia')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = utils.traffic_share(df)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = utils.traffic_city(df)
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:    
    with st.container():
        fig = utils.order_by_week(df)        
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        fig = utils.order_share_by_week(df)
        st.plotly_chart(fig, use_container_width=True)
        
        
with tab3:
    fig = utils.mapa(df)
    st.markdown('#### Localização dos Restaurantes')
    st.plotly_chart(fig, use_container_width=True)