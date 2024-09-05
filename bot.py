import streamlit as st
import google.generativeai as genai
import pandas as pd
from streamlit_chat import message
import csv
from datetime import datetime

# Configure API Key
GOOGLE_API_KEY = "AIzaSyCOEqA_IZlpWCHhMOGaDJ3iJjl5cRmzKgQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "Persona You are a specialist in differential Diagnoses with the name of Dr. House. Only provide information related to health, disease, illness, symptoms, causes, remedies, or medicines."
        "Ask users about their symptoms and provide consultation and guidance based on their input."
        "Always provide brief answers, additionally if the inquiry is not related to health, disease, illness, symptoms, remedies, or medicines politely say Mai aapki Madad Nahi kerskta Shukriya"
        "Always Responses should be in Urdu with English letters"
    )
)

# Function to get response from the chatbot
def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text.strip()

# Set Streamlit page configuration
st.set_page_config(
    page_title="👨‍⚕️ Dr House",
    page_icon="👨‍⚕️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Add background image
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://img.freepik.com/free-photo/blurred-abstract-background-interior-view-looking-out-toward-empty-office-lobby-entrance-doors-glass-curtain-wall-with-frame_1339-6363.jpg');
            background-size: cover;
            background-position: tile;
            background-attachment: fixed;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)


# Load and display a custom header image (optional)
def load_header():
    header_html = """
    <div style="padding:10px;border-radius:10px;text-align:center;">
        <h1 style="margin:0;">👨‍⚕️ Dr House MD</h1>
        <p style="margin:0;">Ask me about your Health related questions!</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False  # Control for displaying the form

# Function to display chat messages
def display_chat_history():
    user_avatar_url = "https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg"
    bot_avatar_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkcIMlZZg9gWdzDQCOvqiN6Ip7yqIsAnvxDw&s"

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
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="{bot_avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
                    <div style="background-color: #128c7E; padding: 10px; border-radius: 10px; max-width: 70%;">
                        <p style="margin: 0;"><b>Bot:</b> {chat['content']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Function to display the booking form
def display_booking_form():
    st.header("Doctor Appointment Booking")
    with st.form("booking_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        booking_date = st.date_input("Date of Booking")
        booking_time = st.time_input("Time of Booking")
        doctor = st.selectbox("Select Doctor", ["Dr. Ali", "Dr. Sara", "Dr. Imran"])
        submit = st.form_submit_button("Book Appointment")

        if submit:
            # Format data and save it to CSV
            appointment_data = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Date": booking_date,
                "Time": booking_time,
                "Doctor": doctor,
            }
            
            # Save to CSV file
            with open("appointments.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=appointment_data.keys())
                # Write header if file is empty
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(appointment_data)

            st.success("Your appointment has been booked successfully!")

# Main application layout
def main():
    load_header()
    st.write("")  # Add spacing

    with st.container():
        display_chat_history()

        if not st.session_state.show_form:  # Only show chat until form is triggered
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
                    
                    # Display chat and response
                    display_chat_history()

                    # If chat is complete, trigger form display
                    if bot_response.lower().contains("appointment") or st.button("End Chat"):
                        st.session_state.show_form = True
                        st.experimental_rerun()

        if st.session_state.show_form:
            display_booking_form()

# Footer
st.markdown("""
    <p style="position: fixed; bottom: 0; width: 100%; text-align: center; font-family: 'Roboto', sans-serif;">
       <a href="https://mwaqasakhtar.eu.org"> Made with ❤️ by Muhammad Waqas (Bravewiki)</a>
    </p>
""", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
