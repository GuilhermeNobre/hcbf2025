import streamlit as st 
import pandas as pd
import numpy as np
import os
import base64
from PIL import Image
from databases.controllers import get_plague_register
from io import BytesIO
from datetime import datetime, timedelta
from functools import lru_cache

# Configuração do cache
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_and_process_image(image_path: str, max_size: tuple = (300, 300)) -> str:
    """
    Carrega e processa uma imagem, redimensionando e comprimindo se necessário.
    Retorna a imagem em formato base64.
    """
    try:
        with Image.open(image_path) as img:
            # Converter para RGB se necessário
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar mantendo a proporção
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Comprimir a imagem
            with BytesIO() as buffer:
                img.save(buffer, format="JPEG", quality=85, optimize=True)
                raw_base64 = base64.b64encode(buffer.getvalue()).decode()
                return f"data:image/jpeg;base64,{raw_base64}"
    except Exception as e:
        st.warning(f"Erro ao processar imagem {image_path}: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_processed_data(num_rows: int, start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
    """
    Obtém e processa os dados do banco de dados com cache.
    """
    data_files = get_plague_register('databases/registers_control.sqlite', num_rows, start_date, end_date)
    database_image = "database_image"
    processed_data = []

    for register in data_files:
        img_id = register[3]
        path_image = os.path.join(database_image, f'{img_id}.jpg')
        comment = register[5] if register[5] is not None else "Nenhuma observação registrada."

        try:
            img_base64 = load_and_process_image(path_image)
            if img_base64:
                processed_data.append({
                    "Preview": img_base64,
                    "Plague": register[1],
                    "Timestamp": datetime.fromtimestamp(register[2]).strftime('%d-%m-%Y'),
                    "Comentario": comment,
                    "Timestamp_unix": register[2]
                })
        except FileNotFoundError:
            st.warning(f"Imagem não encontrada: {path_image}")
            continue

    return pd.DataFrame(processed_data)

def timelife_page():
    st.markdown("""
        <h1>Timelife 📊</h1>
        <p>Histórico completo de todas as pesquisas e detecções realizadas na plataforma.</p>
    """, unsafe_allow_html=True)
    
    # Configurações de filtro de data
    col1, col2 = st.columns(2)
    
    with col1:
        filter_type = st.radio(
            "Tipo de Filtro",
            ["Todos os Registros", "Período", "Data Inicial"],
            horizontal=True
        )
    
    with col2:
        if filter_type == "Período":
            date_range = st.date_input(
                "Selecione o período",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
            if len(date_range) == 2:
                start_date = datetime.combine(date_range[0], datetime.min.time())
                end_date = datetime.combine(date_range[1], datetime.max.time())
            else:
                start_date = datetime.combine(date_range[0], datetime.min.time())
                end_date = datetime.now()
        elif filter_type == "Data Inicial":
            start_date = datetime.combine(
                st.date_input(
                    "Data Inicial",
                    value=datetime.now() - timedelta(days=30),
                    max_value=datetime.now()
                ),
                datetime.min.time()
            )
            end_date = datetime.now()
        else:  # Todos os Registros
            start_date = None
            end_date = None
    
    # Configurações de paginação
    items_per_page = 10
    num_rows = st.slider("Número de registros", 1, 100, items_per_page)
    
    # Carregar dados com cache
    data = get_processed_data(num_rows, start_date, end_date)
    
    if data.empty:
        st.info("Nenhum registro encontrado para o período selecionado.")
        return
    
    # Ordenar dados
    data = data.sort_values(by="Timestamp_unix", ascending=False)
    
    # Exibir informações do período
    if filter_type != "Todos os Registros":
        st.info(f"Mostrando registros de {start_date.strftime('%d/%m/%Y')} até {end_date.strftime('%d/%m/%Y')}")
    else:
        st.info("Mostrando todos os registros disponíveis")
    
    # Configuração das colunas
    config = {
        "Preview": st.column_config.ImageColumn(
            label="Imagem",
            width="medium",
            help="Clique para ampliar"
        ),
        "Plague": st.column_config.TextColumn(
            label="Bacteria",
            width="medium"
        ),
        "Timestamp": st.column_config.TextColumn(
            label="Data/Hora",
            width="small"
        ),
        "Comentario": st.column_config.TextColumn(
            label="Comentário",
            width="large"
        )
    }
    
    # Exibir dados com paginação
    st.dataframe(
        data[["Preview", "Plague", "Timestamp", "Comentario"]],
        column_config=config,
        use_container_width=True,
        hide_index=True
    )