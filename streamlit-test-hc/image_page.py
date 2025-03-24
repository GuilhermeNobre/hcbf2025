import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
from ultralytics import YOLO

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
    print(names_dict)
    print('-------------------')


    probs = result[0].probs.data.tolist()
    print(probs)
    print('-------------------')

    # print(names_dict)
    # print(probs)

    names_and_score = list(zip(names_dict.values(), probs))

    sorted_names_and_score = sorted(names_and_score, key=lambda x: x[1], reverse=True)

    for name, score in sorted_names_and_score:
        print(f"{name}: {score:.6f}")

    # for i in range(len(names_and_score)):
    #     plange_and_score.append((names_and_score[i][0], names_and_score[i][1][0]))

    plague_detected = names_dict[np.argmax(probs)]

    st.header("Analysis 🔍")

    # Exibe as abas
    tab1, tab2 = st.tabs(["Original", "Detected Edges"])
    tab1.image(image, caption="Original", use_container_width=True)
    tab2.image(edges, caption="Detected Edges", use_container_width=True)

    st.title("Praga detectada: " + plague_detected)