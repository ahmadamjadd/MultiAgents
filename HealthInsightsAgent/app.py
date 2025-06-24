import streamlit as st
import os
import uuid
import tempfile
from gtts import gTTS
from deep_translator import GoogleTranslator
from main import app  # your LangGraph app

# --------- Voice Generation ---------
def generate_urdu_voice(text):
    # Translate English to Urdu
    translated_text = GoogleTranslator(source='auto', target='ur').translate(text)
    
    # Generate Urdu speech
    tts = gTTS(text=translated_text, lang='ur')
    temp_audio_path = os.path.join(tempfile.gettempdir(), "urdu_output.mp3")
    tts.save(temp_audio_path)

    return temp_audio_path, translated_text

def play_audio(audio_path):
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

# --------- Streamlit UI ---------
st.set_page_config(page_title="Medical Report Analyzer", page_icon="🩺")
st.title("🩺 Medical Report Analyzer")
st.markdown("Upload a medical report in PDF format. The AI will read, analyze, and explain it in **Urdu** with **audio support**.")

uploaded_file = st.file_uploader("📤 Upload PDF report", type="pdf")

if uploaded_file is not None:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(SCRIPT_DIR, "temp_reports"), exist_ok=True)

    ext = os.path.splitext(uploaded_file.name)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(SCRIPT_DIR, "temp_reports", filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if not os.path.exists(file_path):
        st.error(f"❌ File not found at {file_path}")
    else:
        input_state = {
            "file_path": file_path,
            "messages": []
        }

        if st.button("🔍 Analyze Report"):
            with st.spinner("Analyzing medical report..."):
                try:
                    result = app.invoke(input_state)

                    # English output
                    insights = result["insights"]
                    st.success("✅ Final English Insights:")
                    st.write(insights)

                    # Urdu translation + audio
                    audio_path, urdu_text = generate_urdu_voice(insights)
                    st.markdown("📝 اردو ترجمہ:")
                    st.write(urdu_text)
                    st.markdown("🔊 **آواز میں سنیں:**")
                    play_audio(audio_path)

                except Exception as e:
                    st.error(f"❌ Error: {e}")
