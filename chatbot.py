import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
from PIL import Image
import base64

# Configure API Key
GOOGLE_API_KEY = "AIzaSyCOEqA_IZlpWCHhMOGaDJ3iJjl5cRmzKgQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "Persona You are a heart specialist with the name of Dr. Assad Siddiqui. Only provide information related to heart health, symptoms, and advice."
        "Ask users about their heart-related symptoms and provide consultation and guidance based on their input. "
        "Always provide brief answers, additionaly the inquiry is not related to heart health, politely say that you can only provide heart-related information."
        "Responses should in Urdu written in English."
    )
)

# Function to get response from the chatbot
def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text.strip()

# Set Streamlit page configuration
st.set_page_config(
    page_title="Heart Health Chatbot",
    page_icon="👨‍⚕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Add background image
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://cdn.wallpapersafari.com/29/34/8Ak1Sf.png');
            background-size: cover;
            background-position: tile;
            background-attachment: fixed;
        }
    </style>
""", unsafe_allow_html=True)


# Load and display a custom header image (optional)
def load_header():
    header_html = """
    <div style="padding:10px;border-radius:10px;text-align:center;">
        <h1 style="color:white;margin:0;">Heart Health Chatbot 🫀</h1>
        <p style="color:white;margin:0;">Ask me anything about heart diseases!</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_avatar_url = "https://img.freepik.com/free-photo/sad-cartoon-anatomical-heart_23-2149767987.jpg?t=st=1725263300~exp=1725266900~hmac=3763e175a896a554720d54c6d774dc645dd73078c952913accec719977d50b48&w=740"
bot_avatar_url = "https://img.freepik.com/premium-photo/3d-render-man-doctor-avatar-round-sticker-with-cartoon-character-face-user-id-thumbnail-modern-69_1181551-3160.jpg?w=740"

# Function to display chat messages
def display_chat_history():
    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center;">
                        <div style="background-color: #075e54; padding: 10px; border-radius: 10px; max-width: 70%; ">
                            <p style="margin: 0;"><b>You:</b> {chat['content']}</p>
                        </div>
                        <img src="{user_avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; margin-left: 10px;"/>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # message(chat["content"], avatar_style="bottts")
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="{bot_avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
                    <div style="background-color: #128c7E; padding: 10px; border-radius: 10px; max-width: 70%;">
                        <p style="margin: 0;"><b>Bot:</b> {chat['content']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

 
# Main application layout
def main():
    load_header()
    st.write("")  # Add spacing

    with st.container():
        display_chat_history()

        # User input area
        with st.form(key="user_input_form", clear_on_submit=True):
            user_input = st.text_input(
                label="",
                placeholder="Type your message here...",
                max_chars=500
            )
            submit_button = st.form_submit_button(label="Send")

            if submit_button and user_input.strip():
                with st.spinner("Thinking..."):
                    bot_response = get_chatbot_response(user_input)
                
                # Update chat history
                st.session_state.history.append({"role": "user", "content": user_input})
                st.session_state.history.append({"role": "bot", "content": bot_response})
                st.write(bot_response)
                
                # Refresh chat display
                # st.experimental_rerun()

# Footer
    # <hr style="margin-top: 50px; border: 1px solid #ccc;">
st.markdown("""
    <p style="position: fixed; bottom: 0; width: 100%; text-align: center; font-family: 'Roboto', sans-serif;">
        Made with ❤️ by Assad Siddiqui
    </p>
""", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
