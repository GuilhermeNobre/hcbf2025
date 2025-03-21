import gradio as gr
import numpy as np
from ultralytics import YOLO

model = YOLO("bacteria-yolo11n-cls.pt")

def detect_plague(input_img):
    # sepia_filter = np.array([
    #     [0.393, 0.769, 0.189],
    #     [0.349, 0.686, 0.168],
    #     [0.272, 0.534, 0.131]
    # ]) 
    # sepia_img = input_img.dot(sepia_filter.T)
    # sepia_img /= sepia_img.max() 

    result = model(input_img)
    names_dict = result[0].names
    probs = result[0].probs.data.tolist()

    plague_detected = names_dict[np.argmax(probs)] 
    #print(names_dict[np.argmax(probs)], np.max(probs))

    return plague_detected, gr.update(visible=True)

with gr.Blocks(theme=gr.themes.Soft()) as base_front:
    gr.Markdown("# Plague Detection")
    with gr.Tab("Plague"):
        # image_input = gr.Image(sources=["upload"], label="Upload Image", type="pil")    
        # predict_button = gr.Button("Predict")

        # with gr.Row():
        #     output_text = gr.Textbox(label="Result", scale=2)
        #     with gr.Group(visible=False) as comment_section:
        #         gr.Markdown("## Comments")
        #         comment_area = gr.Textbox(
        #             label="Leave a comment",
        #             placeholder="Type here...",
        #             lines=3
        #         )
                
        #         save_button = gr.Button("Save Comment")

        # predict_button.click(
        #     fn=detect_plague,
        #     inputs=image_input,
        #     outputs=[output_text, comment_section]
        # )

        with gr.Group(visible=False) as comment_section:
            gr.Markdown("## Comments")
            comment_area = gr.Textbox(
                label="Leave a comment",
                placeholder="Type here...",
                lines=3
            )
            
            save_button = gr.Button("Save Comment")

        gr.Interface (
            fn=detect_plague, 
            inputs=gr.Image(
                sources=["upload"], 
                label="Upload Image", 
                type="pil"
            ), 
            outputs=[gr.Textbox(
                label="Result",
                scale=2
                ),comment_section]
        )
    with gr.Tab("TimeLine"):
        pass
    with gr.Tab("Map"):
        pass
    with gr.Tab("About"):  
        pass


base_front.launch(
    share=False, 
    pwa=True
    )

