import streamlit as st
import pandas as pd


from image_page import image_page
from dom_file import *
from map_stream import *
from timelife import *
from landingpage import *
from wikipage import *
from microlife import micro_life_page
from chatbot import chatbot_page

# Configuração da página
st.set_page_config(
    page_title="MicroLife AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


def page1():
    st.title('Page 1')
    st.write('This is page 1')
    df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [10, 20, 30, 40]})
    st.write(df)

def page_map():
    st.title('Page 2')
    st.write('This is page 2')
    df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [10, 20, 30, 40]})
    st.write(df)

def main():
    # Configuração do estilo
    st.markdown("""
        <style>
        :root {
            --background-color: #ffffff;
            --border-color: #e1e4e8;
            --primary-color: #1f77b4;
            --text-color: #262730;
        }
        
        [data-theme="dark"] {
            --background-color: #0e1117;
            --border-color: #262730;
            --primary-color: #4a9eff;
            --text-color: #ffffff;
        }

        .feature-card {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
        }

        /* Seleciona a imagem pelo texto do caption */
        .stImage [alt="logo_dark"] {
            display: block;
        }

        .stImage [alt="logo_light"] {
            display: none;
        }

        [data-theme="dark"] .stImage [alt="logo_dark"] {
            display: none;
        }

        [data-theme="dark"] .stImage [alt="logo_light"] {
            display: block;
        }

        .stCaptionContainer {
            display: none;
        }

        /* Adiciona margem inferior apenas à logo */
        .stImage [alt="logo.png"] {
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Adiciona as imagens usando st.sidebar.image()
    st.sidebar.image("assets/logo.png", use_container_width=True)
    st.sidebar.markdown('<div style="height: 30px; width: 100%;"></div>', unsafe_allow_html=True)
    
    # Menu de navegação
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'Home'
    if st.sidebar.button("🔬 MicroLife AI", use_container_width=True):
        st.session_state.page = 'Microscope'
    # if st.sidebar.button("🦠 Detecção de Bactérias", use_container_width=True):
    #     st.session_state.page = 'Image Page'
    if st.sidebar.button("🗓️ Análise Temporal", use_container_width=True):
        st.session_state.page = 'Time Life'
    if st.sidebar.button("🗺️ Mapeamento", use_container_width=True):
        st.session_state.page = 'Page 2'
    if st.sidebar.button("🔍 Pesquisar", use_container_width=True):
        st.session_state.page = 'Procurar'
    if st.sidebar.button("🤖 Life Bot", use_container_width=True):
        st.session_state.page = 'Life Bot'

    # Adiciona informações na barra lateral
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Sobre o Hub Life")
    st.sidebar.markdown("""
    Plataforma desenvolvida para monitoramento e análise de bactérias humanas.
    
    Versão: 1.0.0
    """)
    st.sidebar.markdown("API Version: [1.0.0](http://136.248.97.106:8000/docs)")

    # Renderiza a página selecionada
    if st.session_state.page == 'Home':
        landing_page_functions()
    if st.session_state.page == 'Image Page':
        image_page()
    elif st.session_state.page == 'Time Life':
        timelife_page()
    elif st.session_state.page == 'Page 2':
        map_page_main()
    elif st.session_state.page == 'Procurar':
        wiki_page_file()
    elif st.session_state.page == 'Microscope':
        micro_life_page()
    elif st.session_state.page == 'Life Bot':
        chatbot_page()

if __name__ == '__main__':
    main()