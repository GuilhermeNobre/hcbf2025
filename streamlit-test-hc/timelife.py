import streamlit as st 
import pandas as pd
import numpy as np
import os
import base64


from PIL import Image
from databases.controllers import get_plague_register
from io import BytesIO
from datetime import datetime

def image_to_base64(img):
    if img:
        with BytesIO() as buffer:
            img.save(buffer, "png")  
            raw_base64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{raw_base64}" 
        

def timelife_page():
    st.write("Timelife all plagues detected")

    num_rows = st.slider("Number of rows", 1, 100, 10)

    data_files = get_plague_register('databases/registers_control.sqlite', num_rows)


    database_image = "database_image" 

    data = []

    for register in data_files:

        img_id = register[3] 
        path_image = os.path.join(database_image, f'{img_id}.jpg')

        try:
            imagem = Image.open(path_image)
            img_base64 = image_to_base64(imagem)
            
            data.append(
                {
                    "Preview": img_base64,
                    "Plague": register[1], 
                    "Timestamp": datetime.fromtimestamp(register[2]).strftime('%d-%m-%Y'),
                    "Timestamp_unix": register[2]
                }
            )
        except FileNotFoundError:
            st.warning(f"Imagem não encontrada: {path_image}")
            continue 

    data = pd.DataFrame(data)

    data = data.sort_values(by="Timestamp_unix", ascending=False)

    config = {
        "Preview": st.column_config.ImageColumn(label="Imagem", width="medium"),
        "Plague": st.column_config.TextColumn(label="Praga"),
        "Timestamp": st.column_config.TextColumn(label="Data/Hora"),
    }

    st.dataframe(data[["Preview", "Plague", "Timestamp"]], column_config=config, use_container_width=True, hide_index=True)