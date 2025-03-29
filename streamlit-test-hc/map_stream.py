import streamlit as st
import streamlit_folium as sf
import folium
import sqlite3
import json
from datetime import datetime
import databases.controllers as db

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
    st.markdown("""
        <h1>MapLife 🗺️</h1>
        <p>Visualização geográfica das áreas mais afetadas por cada tipo de bactéria, permitindo identificar padrões e focos de contaminação.</p>
    """, unsafe_allow_html=True)
    
    m = folium.Map(location=[42.5531, 48.1641], zoom_start=2, disable_3d=True)
    
    # Buscar dados das bactérias
    bacterias_data = get_bacteria_data()
    
    # Adicionar marcadores baseados nos dados reais
    for bacteria in bacterias_data["bacterias"]:
        # Escolher ícone baseado no tipo
        icon = '🦠' if bacteria["tipo"] == "Gram-negativa" else '🧫'
        
        # Criar popup com informações
        popup_text = f"""
            <b>{bacteria['nome']}</b><br>
            Tipo: {bacteria['tipo']}<br>
            Localização: {bacteria['localizacao']}<br>
            Prevalência: {bacteria['prevalencia']}<br>
            Resistência: {bacteria['resistencia']}<br>
            Data: {bacteria['data_deteccao']}<br>
            Coordenadas: {bacteria['latitude']}, {bacteria['longitude']}
        """
        
        # Adicionar o marcador com coordenadas fixas
        folium.Marker(
            location=[bacteria["latitude"], bacteria["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    m.add_child(folium.LatLngPopup())
    sf.st_folium(m, width='100%', height=700)
    
    # st.markdown("### Dados das Bactérias")
    # st.json(bacterias_data)



def map_single_plague(plague_name):
    st.markdown("""
        <h1>MapLife 🗺️</h1>
        <p>Visualização geográfica das áreas mais afetadas por cada tipo de bactéria, permitindo identificar padrões e focos de contaminação.</p>
    """, unsafe_allow_html=True)
    
    m = folium.Map(location=[42.5531, 48.1641], zoom_start=2, disable_3d=True)
    
    bacterias_data = db.get_plague_register_by_plague('databases/plague.db', plague_name)
    print('Data')
    print(bacterias_data)
    pass

    # for bacteria in bacterias_data:
    #     # Escolher ícone baseado no tipo
    #     icon = '🦠' if bacteria["tipo"] == "Gram-negativa" else '🧫'

    #     popupt_text = f"""
    #         <b>{bacteria['plague']}</b><br>
    #         Tipo: {bacteria['tipo']}<br>
    #         Localização: {bacteria['location']}<br>
    #         Data: {bacteria['timestamp']}<br>
    #         Coordenadas: {bacteria['location']}
    #     """



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


    st.title('Map Plague', anchor=False)

    option = st.selectbox(
        "Qual bacteria deseja pesquisar?",
        tuple_name
    )

    if option == "Todas":
        map_all_infos()

    else:
        map_single_plague(option)




