import streamlit as st
from image_page import image_page
from map_stream import *
import pandas as pd


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
    st.sidebar.header('Hub Life 🧬')

    # Inicializa o estado da página
    if 'page' not in st.session_state:
        st.session_state.page = 'Image Page'

    # Botões para mudar a página
    if st.sidebar.button("Plague Detected", icon="🦠"):
        st.session_state.page = 'Image Page'
    if st.sidebar.button("TimeLife", icon="🌱"):
        st.session_state.page = 'Page 1'
    if st.sidebar.button("MapLife", icon="🗺️"):
        st.session_state.page = 'Page 2'

    # Renderiza a página selecionada
    if st.session_state.page == 'Image Page':
        image_page()
    elif st.session_state.page == 'Time Life':
        page1()
    elif st.session_state.page == 'Page 2':
        map_file_to_save()

if __name__ == '__main__':
    main()