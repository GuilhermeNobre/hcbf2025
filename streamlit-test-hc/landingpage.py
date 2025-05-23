import streamlit as st
import sqlite3
import databases.controllers as dbc
import ast

def get_number_of_registers():
    all_register = dbc.get_plague_register('databases/registers_control.sqlite')
    return len(all_register)

def numbers_all_bacterias():
    return 35

def get_number_all_locations():
    all_register = dbc.get_plague_register('databases/registers_control.sqlite')
    list_locations = []
    
    for i in all_register:
        for j in ast.literal_eval(i[4][1:-1]):
            list_locations.append(j)

    return len(list_locations)


def landing_page_functions():
    # print(get_number_of_registers())
    # print(numbers_all_bacterias())
    # get_number_all_locations()

    # Seção de introdução
    st.markdown("""
    <div id="welcome-title">
        <h1>Bem-vindo ao MicroLife AI! 🧬</h1>
        <p>Uma plataforma inteligente para monitoramento e análise de bactérias humanas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cards de funcionalidades
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style='margin-bottom: 30px;'>
                <h3>🔍 Detecção Inteligente</h3>
                <p>Análise automática de bactérias usando IA avançada.</p>
            </div>
            <div>
                <ul style='list-style-type: none; padding-left: 0;'>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>📤 Faça upload de imagens microscópicas</li>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>🔍 Receba análise automática das bactérias</li>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>📊 Visualize as probabilidades de detecção</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style='margin-bottom: 30px;'>
                <h3>📊 Análise Temporal</h3>
                <p>Visualização da evolução das bactérias ao longo do tempo.</p>
            </div>
            <div>
                <ul style='list-style-type: none; padding-left: 0;'>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>📈 Acompanhe a evolução das bactérias</li>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>📊 Visualize tendências e padrões</li>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>🎯 Tome decisões baseadas em dados</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style='margin-bottom: 30px;'>
                <h3>🗺️ Mapeamento</h3>
                <p>Geolocalização e mapeamento das áreas afetadas.</p>
            </div>
            <div>
                <ul style='list-style-type: none; padding-left: 0; '>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>📍 Marque as localizações no mapa</li>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>🌍 Visualize a distribuição geográfica</li>
                    <li style='margin-bottom: 10px; margin-left: 0px;'>⚠️ Identifique áreas críticas</li>
                </ul>
            </div>
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
        st.metric(label="Total de Análises", value=get_number_of_registers())
    
    with col2:
        st.metric(label="Bactérias Detectadas", value=numbers_all_bacterias())
    
    with col3:
        st.metric(label="Áreas Monitoradas", value=get_number_all_locations())