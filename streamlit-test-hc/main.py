import streamlit as st
from image_page import image_page
from dom_file import *
from map_stream import *
import pandas as pd


def landing_page():
    st.title('Hub Life 🧬')
    st.html(title_text_animation())

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
    st.sidebar.header('Hub Life 🧬', anchor=False)

    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    if st.sidebar.button("Home", icon="🏠"):
        st.session_state.page = 'Home'
    if st.sidebar.button("Plague Detected", icon="🦠"):
        st.session_state.page = 'Image Page'
    if st.sidebar.button("TimeLife", icon="🌱"):
        st.session_state.page = 'Time Life'
    if st.sidebar.button("MapLife", icon="🗺️"):
        st.session_state.page = 'Page 2'

    if st.session_state.page == 'Home':
        landing_page()
    if st.session_state.page == 'Image Page':
        image_page()
    elif st.session_state.page == 'Time Life':
        page1()
    elif st.session_state.page == 'Page 2':
        map_file_to_save()

if __name__ == '__main__':
    main()