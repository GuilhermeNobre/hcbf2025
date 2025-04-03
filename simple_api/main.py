from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import numpy as np
from PIL import Image
import io
import cv2
import sys
import os

# Adicionar o diretório streamlit-test-hc ao path do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
streamlit_dir = os.path.join(parent_dir, 'streamlit-test-hc')
sys.path.append(streamlit_dir)

from databases.controllers import get_plague_database
from databases.controllers import get_single_plague_database_like
from databases.controllers import get_single_plague_database

app = FastAPI()

# Carregar o modelo YOLO
model = YOLO(os.path.join(streamlit_dir, 'bacteria-yolo11n-cls.pt'))

@app.get("/list-bacteria")
async def list_bacteria():
    data = get_plague_database(os.path.join(streamlit_dir, "databases/plague.db"))

    data_dict = []
    for dados in data:
        data_dict.append({
            "name": dados[1],
            "characteristics": dados[2],
            "locationManifested": dados[3],
            "diseasesThatAreCaused": dados[4],
            "symptoms": dados[5],
            "medicamentos": dados[6]
        })
    return {"data": data_dict}

@app.get("/list-bacteria/{name}")
async def list_bacteria_name(name):    
    data = get_single_plague_database_like(os.path.join(streamlit_dir, "databases/plague.db"), name)

    data_dict = []
    for dados in data:
        data_dict.append({
            "name": dados[1],
            "characteristics": dados[2],
            "locationManifested": dados[3],
            "diseasesThatAreCaused": dados[4],
            "symptoms": dados[5],
            "medicamentos": dados[6]
        })

    return {"data": data_dict}

@app.post("/detect-bacteria/")
async def detect_bacteria(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        image_array = np.array(image)
        
        edges = cv2.Canny(image_array, 100, 200)
        
        result = model(image_array)
        
        names_dict = result[0].names
        probs = result[0].probs.data.tolist()
        
        names_and_score = list(zip(names_dict.values(), probs))
        names_and_score = [(name, score) for name, score in names_and_score if score > 0.10][:5]
        names_and_score = sorted(names_and_score, key=lambda x: x[1], reverse=True)
        names_and_score = [(name, f"{score*100:.2f}%") for name, score in names_and_score]

        plague_detected = names_dict[np.argmax(probs)]
        dados = get_single_plague_database(os.path.join(streamlit_dir, "databases/plague.db"), plague_detected)

        names_and_score_dict = []
        for names_and_score in names_and_score:
            names_and_score_dict.append({
                "name": names_and_score[0],
                "probability": names_and_score[1]
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "detections": names_and_score_dict,
                "plague_detected": plague_detected,
                "data": {
                    "name": dados[0][1],
                    "characteristics": dados[0][2],
                    "locationManifested": dados[0][3],
                    "diseasesThatAreCaused": dados[0][4],
                    "symptoms": dados[0][5],
                    "medicamentos": dados[0][6]
                }
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Erro ao processar imagem: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 