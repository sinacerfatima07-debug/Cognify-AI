import streamlit as st
import cv2
import numpy as np
import time
import base64
import io
from gtts import gTTS

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="COGNIFY", layout="wide")

# =========================
# BACKGROUND STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: #05060a;
    color: white;
    font-family: Arial;
}

.title {
    text-align:center;
    font-size:3em;
    color:#00f5d4;
    text-shadow:0 0 20px #00f5d4;
}

.footer {
    position:fixed;
    bottom:10px;
    width:100%;
    text-align:center;
    color:rgba(255,255,255,0.4);
    font-size:12px;
}

.glass {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(0,245,212,0.2);
}
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "last_voice" not in st.session_state:
    st.session_state.last_voice = 0
if "eyes_timer" not in st.session_state:
    st.session_state.eyes_timer = None

# =========================
# VOICE SYSTEM
# =========================
def speak(text):
    now = time.time()
    if now - st.session_state.last_voice < 10:
        return

    try:
        tts = gTTS(text=text, lang="en")
        audio = io.BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)

        b64 = base64.b64encode(audio.read()).decode()
        st.markdown(f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

        st.session_state.last_voice = now
    except:
        pass

# =========================
# HOME PAGE
# =========================
if st.session_state.page == "home":
    st.markdown("<div class='title'>🧠 COGNIFY AI</div>", unsafe_allow_html=True)

    st.write("Welcome to AI Monitoring System")

    if st.button("ENTER SYSTEM"):
        speak("Welcome. System activated.")
        st.session_state.page = "scan"
        st.rerun()

# =========================
# SCAN PAGE
# =========================
elif st.session_state.page == "scan":
    st.markdown("<div class='title'>👁️ LIVE SCAN</div>", unsafe_allow_html=True)

    name = st.text_input("User Name", "Fatima Si Nacer")

    cam = st.camera_input("Camera")

    if cam:
        file_bytes = np.asarray(bytearray(cam.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # fake focus score
        focus = np.random.randint(30, 100)

        st.progress(focus / 100)

        if focus < 50:
            st.error("⚠ LOW FOCUS")
            speak("Warning. Focus is low")
        else:
            st.success("OK FOCUS")

        # eye simulation
        eyes_closed = np.random.choice([True, False])

        if eyes_closed:
            if st.session_state.eyes_timer is None:
                st.session_state.eyes_timer = time.time()

            elif time.time() - st.session_state.eyes_timer > 10:
                st.error("👁 Eyes closed too long!")
                speak("Eyes closed detected")
        else:
            st.session_state.eyes_timer = None

    if st.button("BACK"):
        st.session_state.page = "home"
        st.rerun()

# =========================
# FOOTER
# =========================
st.markdown("""
<div class='footer'>
COGNIFY AI • Fatima Si Nacer
</div>
""", unsafe_allow_html=True)
