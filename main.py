import streamlit as st
import base64
from openai import OpenAI
import os
api_key = os.getenv("OPENAI_API_KEY")  # Fetch the API key from environment variables

if api_key:
    openai_client = OpenAI(api_key=api_key)  # Initialize the OpenAI client
else:
    # Raise an error if the API key is not set in the environment variables
    raise ValueError("OPENAI_API_KEY is not set in environment variables!")
# Set your OpenAI API key
# Title of the app
st.image("cookfood.jpg")
st.title("Capture, Click, Cook!")

# Step 1: Capture the image using Streamlit
photo = st.camera_input("Take a picture with your camera:")

if photo is not None:
    # Display the captured photo
    st.image(photo, caption="Captured Photo", use_container_width=True)

    # Step 2: Encode the image in base64 format
    def encode_image_to_base64(image_file):
        return base64.b64encode(image_file.read()).decode("utf-8")

    base64_image = encode_image_to_base64(photo)

    # Step 3: Send the base64 encoded image to the OpenAI API
    with st.spinner("Analyzing the image..."):
        try:
            # Call OpenAI API with the image
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Replace with the appropriate GPT-4 Vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "what can i cook with these ingredient?"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }, 
                    {"role": "system", "content": "you are a cook. you are a cool chef!:) you can first very good recognize the ingredients in the picture, then you can make a super good and simple idea what to cook with these ingredients."}
                ],
                max_tokens=300,
            )

            # Extract and display the model's response
            assistant_message = response.choices[0].message.content
            st.success("Image Analysis:")
            st.write(assistant_message)

        except Exception as e:
            # Handle any errors returned by the API
            st.write ("some thing happend!")
