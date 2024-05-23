from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd
import utils

df_original = pd.read_csv('dataset/train.csv')
df = utils.clean_code(df_original)


import streamlit as st

st.set_page_config(page_title='Marketplace - Visão Restaurantes',  layout='wide',initial_sidebar_state="collapsed")
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
tab1,tab2= st.tabs(['Visão Gerencial',' '])

with tab1:
    with st.container():
        #st.markdown("## Overall Metrics")
        
        col1,col2,col3,col4,col5,col6 = st.columns(6, gap="small")
        
        with col1:
            delivery_unique = len(df['Delivery_person_ID'].unique())
            col1.metric('Entregadores Únicos', delivery_unique)
            
        with col2:
            avg_distance = utils.distance(df, fig=False)            
            col2.metric('Distância Média de Entrega', avg_distance)
            
        with col3:
            avg_festival=utils.entregas(df, 'Yes', 'avg_time')
            col3.metric('Tempo Médio de Entrega c/ Festival', np.round(avg_festival,2), help="Tempo Médio de Entrega c/ Festival")
            
        with col4:
            avg_festival=utils.entregas(df, 'Yes', 'std_time')
            col4.metric('Desvio Padrão de Entrega c/ Festival', np.round(avg_festival,2), help="Desvio Padrão de Entrega c/ Festival")
            
        with col5:
            avg_festival=utils.entregas(df, 'No', 'avg_time')
            col5.metric('Tempo Médio de Entrega s/ Festival', np.round(avg_festival,2), help="Tempo Médio de Entrega s/ Festival")
            
        with col6:
            avg_festival=utils.entregas(df, 'No', 'std_time')
            col6.metric('Desvio Padrão de Entrega s/ Festival', np.round(avg_festival,2), help="Desvio Padrão de Entrega s/ Festival")
    
    
    with st.container():
        
        st.markdown("## Distribuição do Tempo")
        col1,col2, col3 = st.columns(3)
        
        with col1:
            fig = utils.distance(df, fig=True)
            st.plotly_chart(fig, use_container_width=True)
                       
        with col2:
            avg_city=df[['City','Time_taken(min)']].groupby(['City']).agg({'Time_taken(min)': ['mean','std']})
            avg_city.columns = ['avg_time', 'std_time']
            avg_city=avg_city.reset_index()

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Control', x=avg_city['City'],y=avg_city['avg_time'], marker_color= ['rgb(247,252,245)','rgb(116,196,118)','rgb(0,109,44)'], 
                                 error_y=dict(type='data', array=avg_city['std_time'])))
            fig.update_layout(barmode='group')
            fig.update_layout(
                {
                    "height": 451
                }
            )
            st.plotly_chart(fig, use_container_width=True)
          
            
        with col3:

            avg_city_traffic=df[['City','Time_taken(min)','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
            avg_city_traffic.columns = ['avg_time', 'std_time']
            avg_city_traffic=avg_city_traffic.reset_index()

            fig = px.sunburst(avg_city_traffic, path=['City','Road_traffic_density'], values='avg_time',
                              color='std_time',
                              color_continuous_scale='Greens',
                              color_continuous_midpoint=np.average(avg_city_traffic['std_time']),
                              labels={
                                  'std_time': 'Desvio Padrão'
                              }
                             )
            st.plotly_chart(fig, use_container_width=True)
            
            
    with st.container():        
            
        avg_city_traffic_order=df[['City','Time_taken(min)','Type_of_order']].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
        avg_city_traffic_order.columns = ['avg_time', 'std_time']
        avg_city_traffic_order=avg_city_traffic_order.reset_index()

        fig = px.bar(avg_city_traffic_order, x='City', y='avg_time', color='Type_of_order', barmode='group',
                     error_y='std_time', title='Tempo Médio e Desvio Padrão de Entrega por Cidade e Tipo de Pedido',
                     labels={'avg_time': 'Tempo Médio', 'City': 'Cidade', 'Type_of_order': 'Tipo de Pedido'}, 
                     color_discrete_sequence=px.colors.qualitative.Prism
                    )
        fig.update_traces(marker_line_color='black', marker_line_width=2)
        st.plotly_chart(fig, use_container_width=True)

            
    

         