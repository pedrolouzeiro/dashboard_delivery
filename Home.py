import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    layout='wide'
    
)

image = Image.open('images/logo.png')
st.sidebar.image(image, width=120)

st.write("# Delivery Dashboard")

st.markdown( 
    '''
    ##  O dashboard foi construido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes. 
    ### Como utilizar esse Dashboard? 
        ⁃ Visão Empresa: 
            ⁃ Visão Gerencial: Métricas gerais de comportamento. 
            ⁃ Visão Tática: Indicadores semanais de crescimento. 
            ⁃ Visão Geográfica: Insights de geolocalização 
        ⁃ Visão Entregador: 
            ⁃ Acompanhamento dos indicadores semanais de crescimento 
        ⁃ Visão Restaurante: 
            ⁃ Indicadores semanais de crescimento dos restaurantes 
    ### Links         
''')
with st.container():        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            col1.link_button("  Linkedin", "https://www.linkedin.com/in/pedro-henrique-675b31176/")
            
        with col2:            
            col2.link_button("  Projetos", "https://pedrolouzeiro.github.io/portifolio/")
           
        with col3:
            col3.link_button("  Github", "https://github.com/pedrolouzeiro?tab=repositories")
            
        with col4:
            col4.link_button("  Instagram", "https://www.instagram.com/pedrohlribeiro/")

st.sidebar.container(height=230, border=False)
st.sidebar.markdown('## Feito por Pedro Louzeiro')            
