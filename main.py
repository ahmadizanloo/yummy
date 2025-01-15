import streamlit as st
from openai import OpenAI
import os
st.title("snapcook")
st.image("yummy.jpg")
st.markdown('''
<h3>"Hey, what you have in the kitchen?"</h3>
''', unsafe_allow_html=True)  # HTML content for better formatting
#api_key = os.getenv("OPENAI_API_KEY")  # Fetch the API key from environment variables
#if api_key:
 #   openai_client = OpenAI(api_key=api_key)  # Initialize the OpenAI client
#else:
    # Raise an error if the API key is not set in the environment variables
 #   raise ValueError("OPENAI_API_KEY is not set in environment variables!")
SYSTEM_PROMPT = """
"""

if "user_history" not in st.session_state:
    st.session_state.user_history = [{"role": "system", "content": SYSTEM_PROMPT}]
def process_image(image):
    # Handle the image processing here
    if image:
        st.image(image, caption="Here’s your uploaded mystery!", use_column_width=True)
        st.write("Processing your kitchen chaos...")
        # Call your AI model or processing function here
        # Example: result = process_kitchen_image(image)
        # st.write(f"Recipe suggestion: {result}")

st.title("What’s in Your Kitchen?")
st.caption("Upload your kitchen mystery and we’ll solve it deliciously!")

# Camera input
camera_image = st.camera_input("Take a photo of your ingredients!")

# Button to start processing
if st.button("Start the Recipe Magic!"):
    if camera_image:
        process_image(camera_image)
    else:
        st.warning("Please take a photo first!")











