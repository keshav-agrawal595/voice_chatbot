from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
import pyttsx3  # Import pyttsx3 for text-to-speech
import speech_recognition as sr  # Import speech_recognition for speech input

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
def get_gemini_response(question, chat):
    response = chat.send_message(question, stream=True)
    return response

def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak something...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I couldn't understand your speech.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header(f"CONVERSATIONAL Q&A CHATBOT \N{ROBOT FACE} \N{SPEECH BALLOON}")

submit = False

speech_input = st.button("Use Speech Input")

if speech_input:
    input_text = get_speech_input()
    if input_text:
        submit = True
else:
    input_text = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

# Clear chat history at the beginning of each interaction
chat_history = []

if submit and input_text:
    engine = pyttsx3.init()
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=chat_history)
    response = get_gemini_response(input_text, chat)
    # Add user query and response to chat history
    chat_history.append(("You", input_text))
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
    chat_history.append(("Bot", response_text))
    # Speak the response after generating the entire response text
    engine.say(response_text)
    engine.runAndWait()

st.subheader("The Chat History is")
for role, text in chat_history:
    st.write(f"{role}: {text}")

st.markdown("""
<div style='text-align: center; font-size: 25px;'>
Developed with \N{YELLOW HEART}, by <span style='color: cyan; font-weight: 500'>UDAY CHAUHAN</span> and <span style='color: cyan; font-weight: 500'>NIMIT GOYAL</span>
</div>
""", unsafe_allow_html=True)



# Update the line on which it is currenty speaking
# Update the stop button to stop speech module
# Resolve the Speech to automatic speech mode
