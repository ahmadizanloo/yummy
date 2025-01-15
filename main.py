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
# Function to encode the image into base64
def encode_image(uploaded_image):
    return base64.b64encode(uploaded_image.read()).decode("utf-8")

# Streamlit App UI
st.title("SnapCook")
st.caption("Upload your kitchen mystery, and we’ll solve it deliciously!")

# Image Input
uploaded_image = st.file_uploader("Upload a photo of your ingredients!", type=["jpg", "jpeg", "png"])

# Button to start processing
if st.button("Find a Recipe"):
    if uploaded_image:
        try:
            # Encode the uploaded image into base64
            base64_image = encode_image(uploaded_image)

            # Send the image to GPT API
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Replace with your model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What can I cook with the ingredients in this image?",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
            )

            # Extract and display the recipe
            recipe = response.choices[0].message["content"]["text"]
            st.write("### Here's what you can cook:")
            st.write(recipe)

        except Exception as e:
            st.error(f"Error calling GPT API: {str(e)}")
    else:
        st.warning("Please upload a photo first!")
