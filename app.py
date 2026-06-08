import streamlit as st
import json
import time
import re
import os
from groq import Groq

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="Smart PMB Sains Data",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# CLEAN TEXT
# ==================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

# ==================================================
# LOAD DATA & GROQ SETUP
# ==================================================
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Buat System Prompt berdasarkan data.json
system_prompt = f"""Anda adalah asisten virtual cerdas bernama 'Smart PMB Sains Data' dari Universitas PGRI Sumatera Barat.
Tugas Anda adalah memberikan informasi tentang Penerimaan Mahasiswa Baru (PMB) prodi Sains Data.
Jawab dengan ramah, sopan, dan gunakan bahasa Indonesia yang baik, serta gunakan emoji yang relevan.

Berikut adalah informasi resmi yang bisa Anda jadikan referensi utama untuk menjawab:
{json.dumps(data, indent=2)}

Jika pengguna bertanya sesuatu yang tidak ada informasinya di atas atau di luar konteks kampus/Sains Data, sampaikan dengan sopan bahwa Anda hanya melayani pertanyaan terkait PMB Sains Data Universitas PGRI Sumatera Barat. Jangan mengarang informasi.
"""

# ==================================================
# SESSION
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# CSS FINAL (CLEAN MODERN)
# ==================================================
st.markdown("""
<style>

/* FULL BACKGROUND */
.stApp {
    background: #eef3ff;
}

/* HEADER AREA */
.header-box {
    background: linear-gradient(135deg, #002b7f, #0057d8);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 10px;
}

/* CHAT BACKGROUND (FULL, BUKAN KOTAK) */
.chat-area {
    background: #dfe7ff;
    padding: 20px;
    border-radius: 15px;
    min-height: 65vh;
}

/* USER BUBBLE */
.user-bubble {
    background: #0057d8;
    color: white;
    padding: 10px 14px;
    border-radius: 15px 15px 0px 15px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 10px;
}

/* BOT BUBBLE */
.bot-bubble {
    background: white;
    color: black;
    padding: 10px 14px;
    border-radius: 15px 15px 15px 0px;
    max-width: 70%;
    margin-bottom: 10px;
}

/* SIDEBAR (TETAP BIRU LAMA) */
section[data-testid="stSidebar"] {
    background-color: #002b7f;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* BUTTON */
.stButton button {
    width: 100%;
    background-color: #0057d8;
    color: white;
    border-radius: 10px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: gray;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR (TETAP SEPERTI AWAL)
# ==================================================
with st.sidebar:

    st.header("📌 Tentang Chatbot")

    st.write("""
Chatbot ini memberikan informasi:
- biaya kuliah
- pendaftaran
- beasiswa
- fasilitas
- prospek kerja
- dosen
""")

    st.markdown("---")

    st.subheader("📞 Contact Person")
    st.write("👨‍🏫 Zulfaneti - 081363387278")
    st.write("👨‍🏫 Satrio Junaidi - 082389238003")

# ==================================================
# LAYOUT 3 KOLOM
# ==================================================
col1, col2, col3 = st.columns([1, 3, 1])

# ================= LEFT =================
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)

# ================= CENTER =================
with col2:

    # HEADER BOX (GRADIENT)
    st.markdown("""
    <div class='header-box'>
        <h2>🎓 Smart PMB Sains Data</h2>
        <p>Universitas PGRI Sumatera Barat</p>
    </div>
    """, unsafe_allow_html=True)

    # CHAT AREA (FULL BACKGROUND, BUKAN KOTAK PUTIH)
    st.markdown("<div class='chat-area'>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>👤 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>🎓 {msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # INPUT CHAT
    user_input = st.chat_input("Tanyakan tentang PMB Sains Data...")

# ================= RIGHT =================
with col3:
    st.markdown("### 📌 Menu")
    st.write("💰 Biaya Kuliah")
    st.write("📝 Pendaftaran")
    st.write("🎓 Beasiswa")
    st.write("🏫 Fasilitas")
    st.write("💼 Prospek Kerja")

# ==================================================
# CHAT LOGIC
# ==================================================
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("💬 Bot sedang mengetik..."):
        # Menyusun riwayat percakapan untuk dikirim ke Groq
        messages_for_groq = [{"role": "system", "content": system_prompt}]
        
        # Ambil 10 pesan terakhir agar konteks tidak terlalu panjang
        for msg in st.session_state.messages[-10:]:
            messages_for_groq.append({"role": msg["role"], "content": msg["content"]})
            
        try:
            chat_completion = client.chat.completions.create(
                messages=messages_for_groq,
                model="llama-3.1-8b-instant", # Model LLM dari Groq yang lebih baru dan didukung
                temperature=0.3,
                max_tokens=1024,
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            response = f"Maaf 😅 Terjadi kesalahan saat menghubungi server AI: {e}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
