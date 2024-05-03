import streamlit as st
import os
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

import pyaudio

pyaudio_instance = pyaudio.PyAudio()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.text("Listening...")  # Provide feedback
        try:
            audio = r.listen(source, timeout=5)  # Set a timeout
        except Exception as e:
            st.error(f"Error accessing microphone: {e}")
            return None
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand your speech.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")

st.set_page_config(page_title="Q&A Demo")
st.header("CONVERSATIONAL Q&A CHATBOT USING GEMINI API \N{ROBOT FACE} \N{SPEECH BALLOON}")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

submit = False
speech_input = st.checkbox("Use Speech Input")
if speech_input:
    input = get_speech_input()
    if input:
        submit = True
else:
    input = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    response_text = ""
    for chunk in response:
        if hasattr(chunk, 'text'):
            response_text += chunk.text
            st.write(chunk.text)
        elif hasattr(chunk, 'value'):
            response_text += chunk.value
            st.write(chunk.value)
        else:
            st.warning("Invalid response format")
    st.session_state['chat_history'].append(("Bot", response_text))

    # Speak the response
    engine = pyttsx3.init()
    engine.say(response_text)
    engine.runAndWait()

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

st.markdown(""" <div style='text-align: center; font-size: 25px;'> Developed with \N{YELLOW HEART}, using <span style='color: cyan; font-weight: 500'>Gemini</span> and <span style='color: cyan; font-weight: 500'>Streamlit</span> </div> """, unsafe_allow_html=True)
