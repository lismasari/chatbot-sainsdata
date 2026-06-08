import streamlit as st
import json
import time
import re
import os
import base64
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
# FUNCTION TO CONVERT IMAGE TO BASE64
# ==================================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Ambil string base64 dari foto latar belakang
# Ganti "background.jpg" jika nama file foto Anda berbeda
bg_base64 = get_base64_image("background.jpg")

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
if os.path.exists("data.json"):
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
else:
    data = {"info": "Data tidak ditemukan."}

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

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
# CSS DENGAN LATAR BELAKANG FOTO KUSTOM
# ==================================================
css_style = f"""
<style>

/* FULL BACKGROUND FOTO */
.stApp {{
    background-image: url("data:image/jpg;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* OVERLAY TRANSPARAN SUPAYA KONTEN UTAMA TETAP JELAS */
.stApp::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(255, 255, 255, 0.4); /* Efek putih transparan di atas foto */
    z-index: -1;
}}

/* HEADER AREA (GRADIENT) */
.header-box {{
    background: linear-gradient(135deg, rgba(0, 43, 127, 0.95), rgba(0, 87, 216, 0.95));
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}

/* KOTAK CHAT SEMI-TRANSPARAN */
.chat-container-box {{
    background: rgba(255, 255, 255, 0.85); /* Putih transparan agar foto di belakang mengintip sedikit */
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}

/* USER BUBBLE */
.user-bubble {{
    background: #0057d8;
    color: white !important;
    padding: 12px 16px;
    border-radius: 15px 15px 0px 15px;
    max-width: 85%;
    margin-left: auto;
    margin-bottom: 12px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}}

/* BOT BUBBLE */
.bot-bubble {{
    background: #f0f3f9;
    color: #111111 !important;
    padding: 12px 16px;
    border-radius: 15px 15px 15px 0px;
    max-width: 85%;
    margin-bottom: 12px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background-color: rgba(0, 43, 127, 0.95) !important;
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

/* STYLING INPUT CHAT AGAR PAS */
.stChatInput {{
    padding-top: 10px;
}}

</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# ==================================================
# SIDEBAR
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
col1, col2, col3 = st.columns([0.8, 3.4, 0.8])

# ================= LEFT =================
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=110)

# ================= CENTER =================
with col2:
    # HEADER BOX
    st.markdown("""
    <div class='header-box'>
        <h2 style='color: white; margin:0;'>🎓 Smart PMB Sains Data</h2>
        <p style='color: white; margin:5px 0 0 0;'>Universitas PGRI Sumatera Barat</p>
    </div>
    """, unsafe_allow_html=True)

    # Membungkus container chat ke dalam kelas CSS transparan kustom
    st.markdown("<div class='chat-container-box'>", unsafe_allow_html=True)
    
    # Tinggi container 450px menjaga input teks tetap dekat dan tidak terbuang jauh ke bawah
    chat_container = st.container(height=450, border=False)

    with chat_container:
        if not st.session_state.messages:
            st.markdown("<div class='bot-bubble'>🎓 <b>Halo rekan-rekan!</b> Selamat datang di asisten pintar PMB Sains Data Universitas PGRI Sumatera Barat. Ada yang bisa saya bantu hari ini? 😊</div>", unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"<div class='user-bubble'>👤 {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='bot-bubble'>🎓 {msg['content']}</div>", unsafe_allow_html=True)
                    
    st.markdown("</div>", unsafe_allow_html=True)

    # INPUT CHAT langsung menempel di bawah box percakapan
    user_input = st.chat_input("Tanyakan tentang PMB Sains Data...")

# ================= RIGHT =================
with col3:
    # Memberi box putih transparan tipis untuk menu kanan agar tulisan terbaca jelas
    st.markdown("""
    <div style='background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px;'>
        <h3 style='margin-top:0;'>📌 Menu</h3>
        <p>💰 Biaya Kuliah</p>
        <p>📝 Pendaftaran</p>
        <p>🎓 Beasiswa</p>
        <p>🏫 Fasilitas</p>
        <p>💼 Prospek Kerja</p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# CHAT LOGIC
# ==================================================
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with col2:
        with st.spinner("💬 Bot sedang mengetik..."):
            messages_for_groq = [{"role": "system", "content": system_prompt}]
            
            for msg in st.session_state.messages[-10:]:
                messages_for_groq.append({"role": msg["role"], "content": msg["content"]})
                
            try:
                chat_completion = client.chat.completions.create(
                    messages=messages_for_groq,
                    model="llama-3.1-8b-instant",
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
