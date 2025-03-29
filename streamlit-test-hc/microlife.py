import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from ultralytics import YOLO
import pandas as pd
from datetime import datetime
import uuid
from databases.controllers import put_plague_register
import folium
import streamlit_folium as sf
from databases.controllers import get_single_plague_database

# Carregar o modelo YOLO
model = YOLO('bacteria-yolo11n-cls.pt')

def micro_life_page():
    st.markdown("""
        <h1>Micro Life AI 🔬</h1>
        <p>Visualização microscópica das bactérias e análise detalhada das amostras.</p>
    """, unsafe_allow_html=True)

    # Criar duas colunas para layout com larguras iguais
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Captura de Imagem")
        
        # Opção de escolha entre upload e câmera
        input_method = st.radio(
            "Escolha o método de entrada",
            ["Upload de Imagem", "Câmera"],
            horizontal=True
        )
        
        if input_method == "Upload de Imagem":
            # Área para upload de imagem
            uploaded_file = st.file_uploader("Carregar imagem microscópica", type=['jpg', 'jpeg', 'png'])
            
            if uploaded_file is not None:
                try:
                    # Converter o arquivo para imagem
                    image = Image.open(uploaded_file).convert('RGB')
                    st.session_state['uploaded_image'] = image
                except Exception as e:
                    st.error(f"Erro ao carregar a imagem: {e}")
                    return
        else:
            # Usar a câmera nativa do Streamlit
            picture = st.camera_input("Tirar uma foto")
            
            if picture:
                try:
                    # Converter a imagem capturada para array numpy
                    image = Image.open(picture).convert('RGB')
                    st.session_state['uploaded_image'] = image
                except Exception as e:
                    st.error(f"Erro ao processar a imagem: {e}")
                    return
        
        # Botão para iniciar o processo de publicação (agora no final da coluna 1)
        if st.button("Publicar Análize?", use_container_width=True, disabled=not ('uploaded_image' in st.session_state)):
            st.session_state['publish_clicked'] = True

        if 'publish_clicked' not in st.session_state:
            st.session_state['publish_clicked'] = False

        if st.session_state['publish_clicked']:
            st.markdown("### Formulário de Cadastro")
            # Campo para nome da bactéria
            title = st.text_input("Nome da Bactéria", value=st.session_state['plague_title'])
            st.session_state['plague_title'] = title

            # Campo para descrição
            description = st.text_area(
                "Descrição",
                placeholder="Descreva detalhes sobre a bactéria, condições de coleta, observações importantes...",
                height=150
            )
            
            # Mapa para seleção de localização
            st.subheader("Marque os pontos no mapa")
            m = folium.Map(location=st.session_state['map_center'], zoom_start=4)
            m.add_child(folium.LatLngPopup())
                
            # Mostrar marcadores existentes
            for lat, lng in st.session_state['markers']:
                folium.Marker([lat, lng], popup=f"Lat: {lat}, Long: {lng}").add_to(m)
                
            # Mostrar o mapa e capturar cliques
            map_data = sf.st_folium(m, width=1000, height=500)
                
            # Processar cliques no mapa
            if map_data.get("last_clicked"):
                lat = map_data["last_clicked"]["lat"]
                lng = map_data["last_clicked"]["lng"]
                if [lat, lng] not in st.session_state['markers']:
                    st.session_state['markers'].append([lat, lng])
                    st.write(f"Coordenadas capturadas: Latitude {lat}, Longitude {lng}")
                st.session_state['map_center'] = [lat, lng]
                
            # Data da coleta
            date = st.date_input("Quando você viu esta bactéria?")
                
            # Botão para salvar
            if st.button("Salvar dados"):
                if not date:
                    st.error("Por favor, selecione uma data.")
                    return
                if not title:
                    st.error("Por favor, insira um nome.")
                    return
                if not st.session_state['markers']:
                    st.error("Por favor, selecione pelo menos um marcador.")
                    return
                    
                try:
                    # Gerar UUID único
                    uuid_str = str(uuid.uuid4())
                        
                    # Salvar a imagem
                    image.save(f'database_image/{uuid_str}.jpg')
                        
                    # Converter data para timestamp
                    date_string = datetime.strptime(str(date), "%Y-%m-%d").timestamp()
                        
                    # Salvar os dados no banco
                    data = [(title, date_string, uuid_str, str(st.session_state['markers']))]
                    print(data)
                    put_plague_register(data, 'databases/registers_control.sqlite')
                        
                    # Limpar estados
                    st.session_state['publish_clicked'] = False
                    st.session_state['markers'] = []
                    del st.session_state['plague_title']
                        
                    st.success("Dados salvos com sucesso! ✅")
                except Exception as e:
                    print(e)
                    st.error(f"Erro ao salvar os dados: {e}")

    with col2:
        st.markdown("### Análise da Imagem")
        
        if 'uploaded_image' in st.session_state:
            image = st.session_state['uploaded_image']
            image_array = np.array(image)
            
            # Detectar bordas
            edges = cv2.Canny(image_array, 100, 200)
            
            # Fazer a detecção com o modelo YOLO
            result = model(image_array)
            
            # Processar resultados
            names_dict = result[0].names
            probs = result[0].probs.data.tolist()
            
            names_and_score = list(zip(names_dict.values(), probs))
            names_and_score = [(name, score) for name, score in names_and_score if score > 0.10][:5]
            names_and_score = sorted(names_and_score, key=lambda x: x[1], reverse=True)
            names_and_score = [(name, f"{score*100:.2f}%") for name, score in names_and_score]
            
            # Criar DataFrame com os resultados
            df = pd.DataFrame(names_and_score, columns=["Bactéria", "Probabilidade"])
            
            # Identificar a bactéria mais provável
            plague_detected = names_dict[np.argmax(probs)]
            
            # Inicializar variáveis de estado se não existirem
            if 'plague_title' not in st.session_state:
                st.session_state['plague_title'] = plague_detected
            
            if 'markers' not in st.session_state:
                st.session_state['markers'] = []
            
            if 'map_center' not in st.session_state:
                st.session_state['map_center'] = [-15.87680, -47.856445]
            
            if 'publish_clicked' not in st.session_state:
                st.session_state['publish_clicked'] = False
            
            # Mostrar resultados
            st.header("Análise 🔍")
            
            tab1, tab2 = st.tabs(["Original", "Bordas Detectadas"])
            tab1.image(image, caption="Imagem Original", use_container_width=True)
            tab2.image(edges, caption="Bordas Detectadas", use_container_width=True)
            
            st.title("Bactéria detectada: " + plague_detected)
            st.write("Probabilidades:")
            st.write(df)

            st.markdown("---")

            st.title("Informações sobre a bacteria: ")
            dados = get_single_plague_database("./databases/plague.db", plague_detected)
            
            for dados in dados:
                st.write(f"**Nome:** {dados[1]}")
                st.write(f"**Característica:** {dados[2]}")
                st.write(f"**Local Manifestado:** {dados[3]}")
                st.write(f"**Doenças que são causadas:** {dados[4]}")
                st.write(f"**Sintomas:** {dados[5]}")
                st.write(f"**Medicamentos:** {dados[6]}")
                st.write(f"**Dicas:** {dados[7]}")
                st.write(f"**Prevenção:** {dados[8]}")
            
            st.markdown("---")
            
            if st.session_state['publish_clicked']:
                st.markdown("---")