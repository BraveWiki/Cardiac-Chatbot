
from datetime import datetime
import streamlit as st
import google.generativeai as genai
from streamlit_chat import message

# Configure API Key
GOOGLE_API_KEY = "AIzaSyCOEqA_IZlpWCHhMOGaDJ3iJjl5cRmzKgQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "Persona You are a specialist in differential diagnoses with the name of Dr. House. Only provide information related to health, disease, illness, symptoms, causes, remedies, or medicines."
        "Ask users about their symptoms and provide consultation and guidance based on their input."
        "Always provide brief answers, additionally the inquiry is not related to health, disease, illness, symptoms, remedies, or medicines politely say Mai aapki Madad Nahi kerskta Shukriya"
        "Always Responses should be in Urdu with English letters"
    )
)


# Streamlit Interface
st.title("Consult ")

# User input form for heart-related symptoms
with st.form("consultation_form"):
    symptoms = st.text_area("Enter Your Symptoms", height=150)
    submit = st.form_submit_button("Submit")

# Process the form input and get the model's response
if submit:
    # Check if the input is not empty
    if symptoms:
        # Call the generative model to get a response
        response = model.generate(symptoms)

        # Display the model's response
        st.subheader("Consultation Response:")
        st.write(response)
    else:
        st.error("Please enter your symptoms to get a consultation.")
