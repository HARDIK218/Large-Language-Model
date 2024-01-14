from dotenv import load_dotenv
load_dotenv() ## load all the environment variable from .env
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##load gemini pro vision
def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

#streamlit setup
st.set_page_config(page_title = "Invoice image")

st.header("Invoice Application")
input = st.text_input("input prompt: ",key = "input")
uploaded_file = st.file_uploader("choose an image..",type=["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="uploaded Image",use_column_width=True)
submit = st.button("tell me about invoice")

input_prompt = """
you are an expert in understanding invoices.we wll upload a image as invoice and you will have to answer any question based on the uploaded invoice image
"""

#after submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("the response is")
    st.write(response)