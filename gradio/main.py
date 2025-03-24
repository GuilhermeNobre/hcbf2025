import gradio as gr
import numpy as np
from ultralytics import YOLO
from css_python import *


model = YOLO("bacteria-yolo11n-cls.pt")

plague_detected_global = None

def detect_plague(input_img):
    if input_img is None:
        return "Por favor, faça upload de uma imagem.", gr.update(visible=True), gr.update(visible=False)
    
    result = model(input_img)
    names_dict = result[0].names
    probs = result[0].probs.data.tolist()

    plague_detected = names_dict[np.argmax(probs)]
    global plague_detected_global
    plague_detected_global = plague_detected

    return plague_detected, gr.update(visible=True), gr.update(visible=True)


with gr.Blocks(theme=gr.themes.Soft(), css=result_text(), js=title_text_animation()) as base_front:
    # gr.Markdown("# Hub Life 🧬")
    with gr.Tab("Plague"): 
        gr.Markdown("# Plague Detection")
        image_input = gr.Image(sources=["upload"], label="Upload Image", type="pil")    
        predict_button = gr.Button("🔍")

        with gr.Row(equal_height=True, show_progress=True) as output_section:
            output_text = gr.Textbox(label="Result", scale=1, visible=False, elem_id="warning", elem_classes=["feedback"])
            with gr.Group(visible=False) as comment_section:
                comment_area = gr.Textbox(
                    label="Leave a comment",
                    placeholder="Type here...",
                    lines=3
                )
                save_button = gr.Button("🔗")

        predict_button.click(
            fn=detect_plague,
            inputs=image_input,
            outputs=[output_text, output_text, comment_section]  # Atualiza texto e visibilidade
        )

    with gr.Tab("TimeLine"):
        print("TimeLine")
    with gr.Tab("Map"):
        print("Map")
    with gr.Tab("About"):  
        print("About")

base_front.launch(
    share=False, 
    pwa=True
)