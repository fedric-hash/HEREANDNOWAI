import gradio as gr
from my_first_ai_chatbot import get_response
import json
import os

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "branding.json"))) as f:
    brand_info = json.load(f)["brand"]

with gr.Blocks(theme="default", title=brand_info["organizationName"]) as app:
    gr.HTML(f"""<div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="{brand_info["logo"]["title"]}" alt="{brand_info["organizationName"]} Logo" style="height: 100px;">
            </div>""")
    
    gr.ChatInterface(
        fn=get_response,
        chatbot=gr.Chatbot(height=500,
                           avatar_images=(None, brand_info["chatbot"]["avatar"]),
                           type="messages"),
        title=brand_info["organizationName"],
        description=brand_info["slogan"],
        type="messages",
        examples=[
            ["What is AI?"],
            ["Can you explain Reinforcement Learning?"],
            ["How to build a chabot?"],
            ["How long would it take to learn AI?"]
        ]
    )

if __name__ == "__main__":
    app.launch()


