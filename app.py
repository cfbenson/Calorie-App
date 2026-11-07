import os
import io
import base64
import streamlit as st
from PIL import Image
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI Calorie Counter", page_icon="🥗", layout="centered")

st.title("🥗 AI Food & Calorie Tracker")
st.write("Take a photo of your plate or upload an image to analyze its contents and estimate calories.")

input_type = st.radio("Choose input method:", ("Take a Photo", "Upload an Image"), horizontal=True)

image_bytes = None

if input_type == "Take a Photo":
    camera_file = st.camera_input("Take a picture of your food")
    if camera_file:
        image_bytes = camera_file.getvalue()
else:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        st.image(image_bytes, caption="Uploaded Image", use_column_width=True)

if image_bytes:
    if st.button("Analyze Food & Calculate Calories", type="primary"):
        with st.spinner("Analyzing your plate..."):
            try:
                base64_image = base64.b64encode(image_bytes).decode("utf-8")
                
                prompt = (
                    "You are a professional nutritionist. Analyze the food items present in this image. "
                    "Provide a structured breakdown including:\n"
                    "1. Identified food items and estimated portion sizes.\n"
                    "2. Estimated calories per item.\n"
                    "3. Total estimated calorie content.\n"
                    "4. Brief macronutrient summary (Carbs, Protein, Fats).\n"
                    "Keep the tone informative and concise."
                )
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=600,
                )
                
                result = response.choices[0].message.content
                st.success("Analysis Complete!")
                st.markdown("### Results")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
