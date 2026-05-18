import streamlit as st
import json
import time
import re
from rapidfuzz import fuzz

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="Smart PMB Sains Data",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# FUNCTION CLEAN TEXT
# ==================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
.stApp { background-color: #eef3ff; }

.title {
    text-align: center;
    color: #002b7f;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #444;
    font-size: 18px;
    margin-bottom: 25px;
}

section[data-testid="stSidebar"] {
    background-color: #002b7f;
    padding: 20px;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton button {
    width: 100%;
    background-color: #0057d8;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #003080;
}

.chat-container {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #dbe4ff;
}

.user-chat {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
}

.user-bubble {
    background-color: #0057d8;
    color: white;
    padding: 12px;
    border-radius: 18px 18px 0px 18px;
    max-width: 70%;
}

.bot-chat {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 10px;
}

.bot-bubble {
    background-color: #f1f5ff;
    padding: 12px;
    border-radius: 18px 18px 18px 0px;
    max-width: 70%;
    border: 1px solid #dbe4ff;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA JSON
# ==================================================
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# ==================================================
# HEADER
# ==================================================
st.markdown("<div class='title'>🎓 Smart PMB Sains Data</div>", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Chatbot Penerimaan Mahasiswa Baru<br>
Universitas PGRI Sumatera Barat
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.header("📌 Tentang Chatbot")
    st.write("""
Chatbot ini menjawab:
- biaya kuliah
- pendaftaran
- beasiswa
- fasilitas
- prospek kerja
""")

    st.markdown("---")
    st.subheader("📞 Kontak")
    st.write("Zulfaneti - 081363387278")
    st.write("Satrio Junaidi - 082389238003")

# ==================================================
# SESSION CHAT
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# MENU CEPAT
# ==================================================
st.subheader("📌 Menu Cepat")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💰 Biaya Kuliah"):
        prompt = "biaya kuliah"
    elif st.button("📝 Daftar"):
        prompt = "cara daftar"
    else:
        prompt = None

with col2:
    if st.button("🏫 Fasilitas"):
        prompt = "fasilitas"
    elif st.button("💼 Kerja"):
        prompt = "prospek kerja"

with col3:
    if st.button("🎓 Beasiswa"):
        prompt = "beasiswa"
    elif st.button("📞 Kontak"):
        prompt = "kontak"

# ==================================================
# INPUT USER
# ==================================================
user_input = st.chat_input("Tanyakan tentang PMB...")

if user_input:
    prompt = user_input

# ==================================================
# CHAT DISPLAY
# ==================================================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-chat">
            <div class="user-bubble">👤 {msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-chat">
            <div class="bot-bubble">🎓 {msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# CHAT PROCESSING
# ==================================================
if 'prompt' in locals() and prompt:

    clean_prompt = clean_text(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    sapaan = ["halo", "hai", "hello", "hi", "assalamualaikum"]

    response = None

    with st.spinner("🤖 Mencari jawaban..."):
        time.sleep(1)

        # SAPAAN
        if any(word in clean_prompt for word in sapaan):
            response = "Halo 👋 Silakan tanyakan informasi PMB Sains Data."

        else:
            best_score = 0
            best_answer = None

            for item in data:
                for keyword in item["keywords"]:
                    score = fuzz.token_set_ratio(clean_prompt, keyword.lower())

                    if score > best_score:
                        best_score = score
                        best_answer = item["jawaban"]

            # THRESHOLD LEBIH REALISTIS
            if best_score >= 60:
                response = best_answer
            else:
                response = (
                    "Maaf, saya belum menemukan jawaban yang sesuai.\n\n"
                    "Coba tanyakan tentang:\n"
                    "- biaya kuliah\n"
                    "- pendaftaran\n"
                    "- beasiswa\n"
                    "- fasilitas\n"
                    "- prospek kerja"
                )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.markdown("""
<div class='footer'>
🎓 Smart PMB Sains Data UPRIGSBA
</div>
""", unsafe_allow_html=True)
