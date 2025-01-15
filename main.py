import streamlit as st
from openai import OpenAI
import io
import os
import base64

# Initialize OpenAI client (replace YOUR_API_KEY with your OpenAI API key)
api_key = os.getenv("OPENAI_API_KEY")  # Fetch the API key from environment variables

if api_key:
    openai_client = OpenAI(api_key=api_key)  # Initialize the OpenAI client
else:
    # Raise an error if the API key is not set in the environment variables
    raise ValueError("OPENAI_API_KEY is not set in environment variables!")
# Function to send the image to GPT and get a response
def get_recipe_from_image(image):
    try:
        # Convert the image to bytes
        image_bytes = io.BytesIO(image.read())
        encoded_image = "data:image/png;base64," + base64.b64encode(image_bytes).decode()

        # Send the image and prompt to GPT
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model
           messages=[
                {"role": "user", "content": "What can I cook with the ingredients in this image?"}
            ],
            files={"file": ("image.png", image_bytes, "image/png")},
            max_tokens=300
        )
        
        # Extract and return the response
        recommendation = response.choices[0].message["content"]["text"]
        return recommendation
    except Exception as e:
        st.error(f"Error calling GPT API: {str(e)}")
        return None

# Streamlit App UI
st.title("SnapCook")
st.caption("Upload your kitchen mystery, and we’ll solve it deliciously!")

# Image Input
uploaded_image = st.file_uploader("Upload a photo of your ingredients!", type=["jpg", "jpeg", "png"])

# Button to start processing
if st.button("Find a Recipe"):
    if uploaded_image:
        # Call the GPT API with the image
        recommendation = get_recipe_from_image(uploaded_image)
        if recommendation:
            st.write("### Here's what you can cook:")
            st.write(recommendation)
    else:
        st.warning("Please upload a photo first!")
