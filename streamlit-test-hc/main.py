import streamlit as st
from image_page import image_page
from dom_file import *
from map_stream import *
from timelife import *
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Hub Life",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def landing_page():
    # Seção de introdução
    st.markdown("""
    <div id="welcome-title">
        <h1>Bem-vindo ao Hub Life! 🧬</h1>
        <p>Uma plataforma inteligente para monitoramento e análise de bactérias humanas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cards de funcionalidades
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: var(--primary-color);'>🔍 Detecção Inteligente</h3>
            <p>Análise automática de bactérias usando IA avançada.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: var(--primary-color);'>📊 Análise Temporal</h3>
            <p>Visualização da evolução das bactérias ao longo do tempo.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: var(--primary-color);'>🗺️ Mapeamento</h3>
            <p>Geolocalização e mapeamento das áreas afetadas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de como usar
    st.markdown("""
        <div style='margin-top: 30px;'>
            <h3>Como Usar</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Cards de como usar
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: var(--primary-color);'>🦠 Detecção de Bactérias</h3>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 10px;'>📤 Faça upload de imagens microscópicas</li>
                <li style='margin-bottom: 10px;'>🔍 Receba análise automática das bactérias</li>
                <li style='margin-bottom: 10px;'>📊 Visualize as probabilidades de detecção</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: var(--primary-color);'>⏳ Análise Temporal</h3>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 10px;'>📈 Acompanhe a evolução das bactérias</li>
                <li style='margin-bottom: 10px;'>📊 Visualize tendências e padrões</li>
                <li style='margin-bottom: 10px;'>🎯 Tome decisões baseadas em dados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: var(--primary-color);'>🗺️ Mapeamento</h3>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 10px;'>📍 Marque as localizações no mapa</li>
                <li style='margin-bottom: 10px;'>🌍 Visualize a distribuição geográfica</li>
                <li style='margin-bottom: 10px;'>⚠️ Identifique áreas críticas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Seção de estatísticas
    st.markdown("""
        <div style='margin-top: 30px;'>
            <h3>📈 Estatísticas do Sistema</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total de Análises", value="0")
    
    with col2:
        st.metric(label="Bactérias Detectadas", value="0")
    
    with col3:
        st.metric(label="Áreas Monitoradas", value="0")

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
    if st.sidebar.button("🦠 Detecção de Bactérias", use_container_width=True):
        st.session_state.page = 'Image Page'
    if st.sidebar.button("🌱 Análise Temporal", use_container_width=True):
        st.session_state.page = 'Time Life'
    if st.sidebar.button("🗺️ Mapeamento", use_container_width=True):
        st.session_state.page = 'Page 2'

    # Adiciona informações na barra lateral
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Sobre o Hub Life")
    st.sidebar.markdown("""
    Plataforma desenvolvida para monitoramento e análise de bactérias humanas.
    
    Versão: 1.0.0
    """)

    # Renderiza a página selecionada
    if st.session_state.page == 'Home':
        landing_page()
    if st.session_state.page == 'Image Page':
        image_page()
    elif st.session_state.page == 'Time Life':
        timelife_page()
    elif st.session_state.page == 'Page 2':
        map_file_to_save()

if __name__ == '__main__':
    main()