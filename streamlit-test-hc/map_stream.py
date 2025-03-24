import streamlit as st
import streamlit_folium as sf
import folium

def map_file_to_save():
    st.title("MapLife 🗺️", anchor=False)
    m = folium.Map(location=[42.5531, 48.1641], zoom_start=2, disable_3d=True)
    m.add_child(folium.LatLngPopup())

    sf.st_folium(m, width=1000, height=600)