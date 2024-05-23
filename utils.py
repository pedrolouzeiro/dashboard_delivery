import pandas as pd
import plotly.express as px
import numpy as np
from haversine import haversine
import plotly.graph_objects as go


def clean_code(df):
#Recebe DF para limpeza

#1. Remoção de NAN's
    index= df[ (df['Delivery_person_Age'] == "NaN ") |  (df['Road_traffic_density'] == "NaN ") | (df['multiple_deliveries'] == "NaN ") | (df['City'] == "NaN ")].index
    df.drop(index, inplace=True)
    
#2. Remoção de Espaços das strings
    df[["ID","Delivery_person_ID", "Road_traffic_density", "Type_of_order", "Type_of_vehicle", "Festival", "City"]] = df[["ID","Delivery_person_ID", "Road_traffic_density", "Type_of_order", "Type_of_vehicle", "Festival", "City"]].apply(lambda x: x.str.strip())
    df["Weatherconditions"] = df["Weatherconditions"].str.lstrip("conditions ")
    df["Time_taken(min)"] = df["Time_taken(min)"].str.lstrip("(min) ")
    
# 3. Formatação de datas
    df["Order_Date"]=pd.to_datetime(df["Order_Date"],format='%d-%m-%Y')
    df['week_of_year'] = df['Order_Date'].dt.strftime('%U')
    
# 4. Formatação de string em numeros
    df[["Delivery_person_Age", "multiple_deliveries", "Time_taken(min)"]]=df[["Delivery_person_Age", "multiple_deliveries", "Time_taken(min)"]].astype(int)
    df["Delivery_person_Ratings"]=df["Delivery_person_Ratings"].astype(float)
    
#Retorna DF
    return df


def pedidos_por_dia(df):
    qtd_dia=df.groupby(['Order_Date'])['ID'].count().to_frame('qtd').reset_index()
    fig = px.bar(qtd_dia, x='Order_Date', y='qtd',color="qtd",labels={
        'Order_Date': 'Data do pedido',
        'qtd': 'Quantidade'
    }, text='qtd',color_continuous_scale='greens')

    fig.update_traces(textposition='inside')#,texttemplate='%{text:.2s}')
    fig.update_yaxes(showticklabels=False,showgrid=False,)
    return fig


def traffic_share(df):   
    tipo_trafego=df.groupby(["Road_traffic_density"])['ID'].count().to_frame('qtd').reset_index()

    fig = px.pie(tipo_trafego, values='qtd', names='Road_traffic_density',title="Quantidade de Pedidos por Tráfego",color_discrete_sequence=['rgb(116,196,118)','rgb(0,109,44)'])
    return fig

def traffic_city(df):
    cidade_trafego=df.groupby(['City','Road_traffic_density'])['ID'].count().to_frame('qtd').reset_index()

    fig = px.scatter(cidade_trafego, 
                        x="City",
                        y="Road_traffic_density",
                        size="qtd",size_max=60, 
                        title="Quantidade de Pedidos por Tráfego e Cidade",                        
                        color_discrete_sequence=['rgb(161,217,155)','rgb(35,139,69)','rgb(0,68,27)'],
                        labels={
                        'City': 'Cidade',
                        'Road_traffic_density': 'Densidade de Tráfego'  
                        }
                    )
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False, zeroline=False)
    return fig
        
def order_by_week(df):
    qtd_semana=df.copy()
    qtd_semana=qtd_semana.groupby(['week_of_year'])['ID'].count().reset_index()
    fig = px.line(qtd_semana, 
            x='week_of_year', 
            y='ID', 
            text="ID",
            title="Pedidos por Semana",
            labels={
                'week_of_year': 'Semana do Ano'
    })
    fig.update_traces(textfont_color="#00ff00",textposition='top center',line={'width': 2,'color':'rgb(0,68,27)'})#textfont_size=12,
    #line color line width
    fig.update_xaxes(
        showline=True,  # Mostra linhas
        showgrid=False,  # Não mostra grades
        showticklabels=True  # Mostra rótulos
    )

    fig.update_yaxes(showticklabels=False,title_font_color="rgba(0, 0, 0, 0)",showgrid=False, zeroline=False)
    return fig
    
def order_share_by_week(df):
    qtd_semana=df.copy()
    qtd_semana=qtd_semana.groupby(['week_of_year'])['ID'].count().reset_index()
    ped_por_semana= df.groupby(['week_of_year'])['Delivery_person_ID'].nunique().to_frame('qtd').reset_index()
    ped_por_semana['qtd']=qtd_semana['ID']/ped_por_semana['qtd']
    ped_por_semana['qtd']=np.round(ped_por_semana['qtd'], 2)
        
    fig = px.line(ped_por_semana, 
            x='week_of_year', 
            y='qtd', 
            text='qtd', 
            title="Média de Pedidos por Semana",
            labels={
            'qtd': 'Média',
            'week_of_year': 'Semana do Ano'
    })

    fig.update_traces(textfont_color="#00ff00",textposition='top center',line={'width': 2,'color':'rgb(0,68,27)'})#textfont_size=12,
        #line color line width
    fig.update_xaxes(
        showline=True,  # Mostra linhas
        showgrid=False,  # Não mostra grades
        showticklabels=True  # Mostra rótulos
    )

    fig.update_yaxes(showticklabels=False,title_font_color="rgba(0, 0, 0, 0)",showgrid=False, zeroline=False)
    return fig
    
    
def mapa(df):
    localiza = df[['City', 'Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']]
    localiza=localiza.groupby(['City','Road_traffic_density']).median().reset_index()

    fig = px.scatter_mapbox(localiza, lat="Delivery_location_latitude", lon="Delivery_location_longitude",
                            color_discrete_sequence=["fuchsia"], zoom=6, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def top(df, ordem):
    tp=df[['Delivery_person_ID','City', 'Time_taken(min)']]
    tp=tp.groupby(['City','Delivery_person_ID'])['Time_taken(min)'].mean().reset_index()
    tp=tp.sort_values(['City','Time_taken(min)'], ascending=ordem)

    tp_fast_met=tp.loc[(tp['City'] == 'Metropolitian')].head(10)
    tp_fast_ur=tp.loc[(tp['City'] == 'Urban')].head(10)
    tp_fast_sem=tp.loc[(tp['City'] == 'Semi-Urban')].head(10)

    tp= pd.concat([tp_fast_met,tp_fast_ur,tp_fast_sem])
    tp=tp.reset_index(drop=True)
    return tp


def entregas(df, yn, avg_std):
    avg_festival=(df[['Time_taken(min)','Festival']]
                    .groupby('Festival')
                    .agg({'Time_taken(min)': ['mean','std']}))
            
    avg_festival.columns = ['avg_time', 'std_time']
    avg_festival=avg_festival.reset_index()
    avg_festival = avg_festival.loc[avg_festival['Festival'] == yn, avg_std]
            
    return avg_festival


def distance(df, fig):
    if fig == False:
        cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude','Restaurant_longitude']
        df['distance'] = df[cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis = 1)            
        avg_distance = np.round(df['distance'].mean(),2)
        return avg_distance
    else:
        cols = ['Delivery_location_latitude','Delivery_location_longitude','Restaurant_latitude','Restaurant_longitude']

        df['distance'] = df[cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis = 1)

        avg_distance=df[['City','distance']].groupby('City').mean().reset_index()

        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'],marker_colors=['rgb(247,252,245)','rgb(116,196,118)','rgb(0,109,44)'], values=avg_distance['distance'],pull=[0, 0.1, 0])])
        return fig
