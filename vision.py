import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Set the page configuration
st.set_page_config(page_title="Image Analysis Application", page_icon=":camera:", layout="wide")

# Apply custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: black;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-size: 3em;
        color: #ff4b4b;
        text-align: center;
    }
    .header {
        text-align: center;
        font-size: 2em;
        color: #4b8bff;
    }
    .subheader {
        font-size: 1.5em;
        color: #000000;
    }
    .input {
        font-size: 1.2em;
    }
    .button {
        background-color: #ff4b4b;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        font-size: 1.2em;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Add a title
st.markdown('<p class="title">Image Analysis Application</p>', unsafe_allow_html=True)

# Get the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set the GOOGLE_API_KEY in the .env file.")

# Function to get response from Gemini API
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel("gemini-1.5-pro")
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

# Create two columns with the specified ratio
col1, col2, col3= st.columns([3,1, 6])

with col1:
    # Input section on the left
    st.markdown('<p class="header">Insert Image</p>', unsafe_allow_html=True)
    
    # Input text box
    input_text = st.text_input("Input Prompt:", key="input", placeholder="Enter a prompt...", help="Describe what you want to know about the image.")
    
    # File uploader
    upload_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        image = None
    
    # Submit button
    submit_button = st.button("Tell me about the image", key="submit", help="Click to analyze the image")

with col2:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

with col3:
    # Output section on the right
    st.markdown('<p class="header">Generated Response</p>', unsafe_allow_html=True)

    if submit_button:
        if image is not None:
            with st.spinner("Analyzing the image..."):
                response = get_gemini_response(input_text, image)
                st.markdown('<p class="subheader">Here is the information:</p>', unsafe_allow_html=True)
                st.write(response)
        else:
            st.warning("Please upload an image before submitting.")

# Footer
st.markdown("---")
st.markdown('<p class="subheader">Powered by Google Gemini API</p>', unsafe_allow_html=True)
