import streamlit as st
import streamlit_folium as sf
import folium

def map_file_to_save():
    if "markers" not in st.session_state:
        st.session_state.markers = []

    m = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)
    m.add_child(folium.LatLngPopup())

    for lat, lng in st.session_state.markers:
        folium.Marker([lat, lng], popup=f"Lat: {lat}, Long: {lng}").add_to(m)

    map_data = sf.st_folium(m, width=1000, height=500)

    if map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]
        if [lat, lng] not in st.session_state.markers:
            st.session_state.markers.append([lat, lng])
            st.write(f"Coordenadas capturadas: Latitude {lat}, Longitude {lng}")

        print(st.session_state.markers)