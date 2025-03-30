import streamlit as st
import streamlit_folium as sf
import folium
import sqlite3
import json
import databases.controllers as db
import ast
import pandas as pd
import pydeck as pdk
from datetime import datetime
from folium.plugins import HeatMap
from datetime import datetime

def get_bacteria_data():
    conn = sqlite3.connect('databases/registers_control.sqlite')
    cursor = conn.cursor()
    
    # Buscar dados das bactérias incluindo a localização
    cursor.execute("""
        SELECT Plague, Timestamp, id, location 
        FROM registers 
        ORDER BY Timestamp DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    # Processar os dados
    bacterias = []
    for plague, timestamp, id, location in results:
        # Converter timestamp para data legível
        date_str = datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d')
        
        # Determinar tipo e localização baseado no nome da praga
        tipo = "Gram-negativa" if any(b in plague.lower() for b in ['e. coli', 'klebsiella', 'pseudomonas']) else "Gram-positiva"
        localizacao = "Intestino" if any(b in plague.lower() for b in ['e. coli', 'enterococcus']) else "Trato Respiratório"
        
        # Determinar prevalência baseado na data
        data_obj = datetime.strptime(date_str, '%Y-%m-%d')
        dias_antigos = (datetime.now() - data_obj).days
        prevalencia = "Alta" if dias_antigos < 30 else "Média" if dias_antigos < 90 else "Baixa"
        
        # Determinar resistência baseado no tipo
        resistencia = "Múltipla" if tipo == "Gram-negativa" else "MRSA" if "staphylococcus" in plague.lower() else "Vancomicina"
        
        # Processar as coordenadas
        try:
            coords = json.loads(location)
            # Usar a primeira coordenada do array como localização principal
            for coord in coords:
                lat, lon = coord
                bacterias.append({
                    "nome": plague,
                    "tipo": tipo,
                    "localizacao": localizacao,
                    "prevalencia": prevalencia,
                    "resistencia": resistencia,
                    "data_deteccao": date_str,
                    "uuid": str(id),
                    "latitude": lat,
                    "longitude": lon
                })
        except (json.JSONDecodeError, IndexError):
            # Se houver erro ao processar as coordenadas, usar valores padrão
            lat, lon = 0, 0
        
        
    
    return {"bacterias": bacterias}

def map_all_infos():
    # st.markdown("""
    #     <h1>MapLife 🗺️</h1>
    #     <p>Visualização geográfica das áreas mais afetadas por cada tipo de bactéria, permitindo identificar padrões e focos de contaminação.</p>
    # """, unsafe_allow_html=True)
    
    m = folium.Map(location=[-9.8975, -50.3613], zoom_start=3, disable_3d=True)
    

    bacterias_data = get_bacteria_data()
    
    for bacteria in bacterias_data["bacterias"]:
        
        #icon = '🦠' if bacteria["tipo"] == "Gram-negativa" else '🧫'
        
        lat_format = "{:.3f}".format(bacteria["latitude"])
        lon_format = "{:.3f}".format(bacteria["longitude"])

        popup_text = f"""
            <b>{bacteria['nome']}</b><br>
            Data: {bacteria['data_deteccao']}<br>
            Coordenadas: {lat_format}, {lon_format}
        """
        # Localização: {bacteria['localizacao']}<br> 
        # Adicionar o marcador com coordenadas fixas
        folium.Marker(
            location=[bacteria["latitude"], bacteria["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    m.add_child(folium.LatLngPopup())
    sf.st_folium(m, width='100%', height=1000)
    
    # st.markdown("### Dados das Bactérias")
    # st.json(bacterias_data)



def map_single_plague(plague_name):

    m = folium.Map(location=[-9.8975, -50.3613], zoom_start=2, disable_3d=True)
    
    bacterias_data = db.get_plague_register_by_plague('databases/registers_control.sqlite', plague_name)
    
    #print(bacterias_data)
    #print('----------------')
    if len(bacterias_data) == 0:
        st.error("Nenhuma informação encontrada para a praga selecionada")
        return
    #print('Data')
    #print(bacterias_data)

    name_plague = bacterias_data[0][1]
    #print(name_plague) 

    locations_info = []

    for i in range(len(bacterias_data)):
        for j in ast.literal_eval(bacterias_data[i][4]):
            #j.append(bacterias_data[i][2].strftime('%d-%m-%Y')) # (register[2]).strftime('%d-%m-%Y')
            j.append(datetime.fromtimestamp(bacterias_data[i][2]).strftime('%d-%m-%Y'))
            j.append(bacterias_data[i][5])
            locations_info.append(j)
        
    

    #print(locations_info)
    #print(locations_info)

    for i in range(len(locations_info)):

        location_a = "{:.3f}".format(locations_info[i][0])
        location_b = "{:.3f}".format(locations_info[i][1])

        popup_text = f"""
            <b>{name_plague}</b><br>
            Coordenadas: {location_a}, {location_b}<br>
            Data: {locations_info[i][2]}<br>
            Observação: {locations_info[i][3]}
        """

        folium.Marker(
            location=[locations_info[i][0], locations_info[i][1]],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    m.add_child(folium.LatLngPopup())
    sf.st_folium(m, width='100%', height=700)

# def heatmap_all():
#     m = folium.Map([42.5531, 48.1641], zoom_start=2)

#     bacterias_data = get_bacteria_data() 

#     heatmap_data = [
#         [bacteria["latitude"], bacteria["longitude"]]
#         for bacteria in bacterias_data["bacterias"]
#     ]

#     # print(heatmap_data)
#     #print("HeatMap")
#     heatmap_data = [[40.7128, -74.0060], [34.0522, -118.2437], [51.5074, -0.1278]]
#     HeatMap(heatmap_data).add_to(m)
#     #print(HeatMap(heatmap_data).add_to(m))
#     sf.st_folium(m, width='100%')
#     # folium_static(m)


def heatmap_all():

    bacterias_data = get_bacteria_data()

    # Prepare the data in a format suitable for pydeck
    heatmap_data = [
        {"lat": bacteria["latitude"], "lon": bacteria["longitude"]}
        for bacteria in bacterias_data["bacterias"]
    ]

    COLOR_BREWER_MODIFIED_SCALE = [
        [204, 255, 204],  
        [230, 255, 204], 
        [255, 255, 153],  
        [255, 230, 102],  
        [255, 153, 102],  
        [255, 51, 51],   
    ]

    #print(heatmap_data)
    #print('----------------')

    

    layer = pdk.Layer(
        "HeatmapLayer",
        data=heatmap_data,
        get_position=["lon", "lat"],
        radius_pixels=45,
        opacity=1,
        aggregation="MEAN",
        color_range=COLOR_BREWER_MODIFIED_SCALE,
    )


    view_state = pdk.ViewState(
        latitude=-12.8975,
        longitude=-50.3613,
        zoom=2,
        pitch=0
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9"  # Optional: requires Mapbox token
    )


    st.pydeck_chart(r)


def heat_map_single_plague(plague_name):
    bacterias_data = db.get_plague_register_by_plague('databases/registers_control.sqlite', plague_name)

    if len(bacterias_data) == 0:
        st.error("Nenhuma informação encontrada para a praga selecionada")
        return

    locations_info = []

    for i in range(len(bacterias_data)):
        for j in ast.literal_eval(bacterias_data[i][4]):
            # print(j) 
            locations_info.append(j)

    locations_list = [] # This is [[37.92686760148135, 35.91430664062501], [36.778492404594154, 34.24987792968751], [37.67077737288316, 36.64489746093751], [-19.93075031142836, -40.23468006514012], [8.320211206699756, -10.283200893401975], [11.695271624635724, -8.525387835502448], [20.0559305042887, -23.2031232136487], [18.729500983002968, 78.92578737080136], [-23.483402337004417, -50.185544337630134], [-19.476951223034515, -58.62304470777499], [-26.667094933426775, -55.19531154513354], [-10.574223069716929, -57.48046665787685], [-14.604848374958255, -58.007810440063345], [-3.776560701596921, -71.71874751090989], [-13.976715490905367, -39.39697221100328], [-0.5273368144096696, -62.22656121253961]]
    #[[37.92686760148135, 35.91430664062501], [36.778492404594154, 34.24987792968751], [37.67077737288316, 36.64489746093751], [-19.93075031142836, -40.23468006514012], [8.320211206699756, -10.283200893401975], [11.695271624635724, -8.525387835502448], [20.0559305042887, -23.2031232136487], [18.729500983002968, 78.92578737080136], [-23.483402337004417, -50.185544337630134], [-19.476951223034515, -58.62304470777499], [-26.667094933426775, -55.19531154513354], [-10.574223069716929, -57.48046665787685], [-14.604848374958255, -58.007810440063345], [-3.776560701596921, -71.71874751090989], [-13.976715490905367, -39.39697221100328], [-0.5273368144096696, -62.22656121253961]]

    for i in range(len(locations_info)):
        locations_list.append([locations_info[i][0], locations_info[i][1]]) 

    final_list = []
    for i in range(len(locations_list)):
        final_list.append({"lat": locations_list[i][0], "lon": locations_list[i][1]})

    #print(final_list)



    COLOR_BREWER_MODIFIED_SCALE = [
        [204, 255, 204],  
        [230, 255, 204], 
        [255, 255, 153],  
        [255, 230, 102],  
        [255, 153, 102],  
        [255, 51, 51],   
    ]

    # Create the heatmap layer
    layer = pdk.Layer(
        "HeatmapLayer",
        data=final_list,
        get_position=["lon", "lat"],
        radius_pixels=45,
        opacity=1,
        aggregation="MEAN",
        color_range=COLOR_BREWER_MODIFIED_SCALE,
    )

    # Set the initial view state
    view_state = pdk.ViewState(
        latitude=-9.8975,
        longitude=-50.3613,
        zoom=2,
        pitch=0
    )

    # Create the deck.gl visualization
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9"  # Optional: requires Mapbox token
    )

    # Display in Streamlit
    st.pydeck_chart(r)



def map_page_main(): 
    data_from_db = db.get_plague_database('databases/plague.db')

    tuple_name = ()
    for i in range(len(data_from_db)):
        tuple_name += (data_from_db[i][1],)

    #print(tuple_name)

    temp_list = list(tuple_name)

    temp_list.insert(0, "Todas")

    tuple_name = tuple(temp_list)

    #print(tuple_name) 

    st.markdown("""
        <h1>MapLife 🗺️</h1>
        <p>Visualização geográfica das áreas mais afetadas por cada tipo de bactéria, permitindo identificar padrões e focos de contaminação.</p>
    """, unsafe_allow_html=True)
    

    option = st.selectbox(
        "Qual bacteria deseja pesquisar?",
        tuple_name
    )

    if option == "Todas":
        tab1, tab2 = st.tabs(["Mapa de Marcadores", "Mapa de Calor"])
        
        with tab1:
            map_all_infos()
        with tab2:
            heatmap_all()

    else:

        tab1, tab2 = st.tabs(["Mapa de Marcadores", "Mapa de Calor"])

        with tab1:
            map_single_plague(option)
        with tab2:
            heat_map_single_plague(option)




