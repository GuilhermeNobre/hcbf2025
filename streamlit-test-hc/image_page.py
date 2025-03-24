import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
from ultralytics import YOLO
import pandas as pd
import streamlit_folium as sf
import folium

model = YOLO('bacteria-yolo11n-cls.pt')

def image_page():
    st.title('Image Page')
    st.write("Streamlit is also great for more traditional ML use cases like computer vision or NLP. Here's an example of edge detection using OpenCV. 👁️")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert('RGB')  # Converte para RGB
            st.session_state['uploaded_image'] = image
        except Exception as e:
            st.error(f"Erro ao carregar a imagem: {e}")
            return
    else:
        if 'uploaded_image' not in st.session_state:
            st.write("Nenhuma imagem enviada.")
            return
        else:

            image = st.session_state['uploaded_image']


    image_array = np.array(image)
    edges = cv2.Canny(image_array, 100, 200)

    result = model(image_array)

    names_dict = result[0].names
    probs = result[0].probs.data.tolist()

    names_and_score = list(zip(names_dict.values(), probs))

    names_and_score = [(name, score) for name, score in names_and_score if score > 0.10][:5]

    names_and_score = sorted(names_and_score, key=lambda x: x[1], reverse=True)

    names_and_score = [(name, f"{score*100:.2f}%") for name, score in names_and_score]

    
    print(names_and_score)

    df = pd.DataFrame(names_and_score, columns=["Plague", "Score"])

    plague_detected = names_dict[np.argmax(probs)]

    st.header("Analysis 🔍")

    tab1, tab2 = st.tabs(["Original", "Detected Edges"])
    tab1.image(image, caption="Original", use_container_width=True)
    tab2.image(edges, caption="Detected Edges", use_container_width=True)

    st.title("Praga detectada: " + plague_detected)

    st.write("Probabilidades:")
    st.write(df)

    if 'plague_title' not in st.session_state:
        st.session_state['plague_title'] = plague_detected
    if 'publish_clicked' not in st.session_state:
        st.session_state['publish_clicked'] = False
    if 'markers' not in st.session_state:
        st.session_state['markers'] = []
    if 'map_center' not in st.session_state:
        st.session_state['map_center'] = [-15.87680, -47.856445]

    if st.button("Publish data?"):
        st.session_state['publish_clicked'] = True

    if st.session_state['publish_clicked']:
        title = st.text_input("Plague Name", value=st.session_state['plague_title'], key="plague_title_input")
        st.session_state['plague_title'] = title

        st.subheader("Marque os pontos no mapa")
        m = folium.Map(location=st.session_state['map_center'], zoom_start=12)
        m.add_child(folium.LatLngPopup())

        for lat, lng in st.session_state['markers']:
            folium.Marker([lat, lng], popup=f"Lat: {lat}, Long: {lng}").add_to(m)

        map_data = sf.st_folium(m, width=1000, height=500)

        if map_data.get("last_clicked"):
            lat = map_data["last_clicked"]["lat"]
            lng = map_data["last_clicked"]["lng"]
            if [lat, lng] not in st.session_state['markers']:
                st.session_state['markers'].append([lat, lng])
                st.write(f"Coordenadas capturadas: Latitude {lat}, Longitude {lng}")
            st.session_state['map_center'] = [lat, lng]

        # Botão "Save data"
        if st.button("Save data"):
            title = st.session_state['plague_title']
            markers = st.session_state['markers']
            print(f"Praga: {title}")
            print(f"Pontos: {markers}")
            st.write("Dados salvos com sucesso!")
            st.session_state['publish_clicked'] = False
            st.session_state['markers'] = []
            st.success('This is a success message!', icon="✅")
