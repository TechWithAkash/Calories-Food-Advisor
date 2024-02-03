import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
load_dotenv()  # load all the Environment Variables

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been Uploaded
    if uploaded_file is not None:
        # Read the File into bytes
        bytes_data = uploaded_file.getvalue()

        images_parts = [
            {
                'mime_type': uploaded_file.type,  # Get mime type of the Uploaded file
                'data': bytes_data
            }
        ]
        return images_parts
    else:
        raise FileNotFoundError("NO File Uploaded")


# Initialize the Streamlit APP for UI Perspective
st.set_page_config(page_title="Gemini Health App")
st.header(" Health Advisor App👨‍⚕️👨‍⚕️")
uploaded_file = st.file_uploader("Choose an Image...", type=['jpg', 'jpeg', 'png'])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the total calories")

# Input Prompt Decide how the Google gemin Model React like
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               Finally you can also Mention whether food is healthy or not
"""

## If submit button is clicked
if submit:
    # Move these lines inside the if block
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("The Response is😍")
    st.write(response)
