import streamlit as st
from datetime import datetime
import genai  # Assuming you're using the 'genai' package for the generative model

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "Persona: You are a heart specialist with the name of Dr. Assad Siddiqui. Only provide information related to heart health, symptoms, and advice. "
        "Ask users about their heart-related symptoms and provide consultation and guidance based on their input. "
        "Always provide brief answers, additionally, if the inquiry is not related to heart health, politely say that you can only provide heart-related information. "
        "Responses should be in Urdu written in English."
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
        st.error("Please enter your heart-related symptoms to get a consultation.")
