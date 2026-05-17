import streamlit as st
import json
from rapidfuzz import fuzz
import time

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="Smart PMB Sains Data",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f4f8ff;
}

/* Judul */
.title {
    text-align: center;
    color: #003b8e;
    font-size: 40px;
    font-weight: bold;
}

/* Subjudul */
.subtitle {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #003b8e;
}

/* Tombol */
.stButton button {
    width: 100%;
    background-color: #0057d8;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #003080;
    color: white;
}

/* CHAT USER (KANAN) */
.user-chat {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 15px;
}

.user-bubble {
    background-color: #0057d8;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 0px 18px;
    max-width: 70%;
    font-size: 15px;
}

/* CHAT BOT (KIRI) */
.bot-chat {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 15px;
}

.bot-bubble {
    background-color: white;
    color: black;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 0px;
    max-width: 70%;
    border: 1px solid #dbe4ff;
    font-size: 15px;
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA JSON
# ==================================================
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# ==================================================
# LOGO
# ==================================================
try:
    st.image("logo.png", width=120)
except:
    pass

# ==================================================
# HEADER
# ==================================================
st.markdown(
    "<div class='title'>🎓 Smart PMB Sains Data UPRIGSBA</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
    Chatbot Penerimaan Mahasiswa Baru <br>
    Program Studi Sains Data Universitas PGRI Sumatera Barat
    </div>
    """,
    unsafe_allow_html=True
)

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
- dan informasi lainnya
""")

    st.markdown("---")

    st.subheader("📞 Contact Person")

    st.write("👨‍🏫 Zulfaneti")
    st.write("081363387278")

    st.write("👨‍🏫 Satrio Junaidi")
    st.write("082389238003")

# ==================================================
# MENU CEPAT
# ==================================================
st.subheader("📌 Menu Cepat")

col1, col2, col3 = st.columns(3)

with col1:
    biaya_btn = st.button("💰 Biaya Kuliah")
    daftar_btn = st.button("📝 Cara Daftar")

with col2:
    fasilitas_btn = st.button("🏫 Fasilitas")
    kerja_btn = st.button("💼 Prospek Kerja")

with col3:
    kip_btn = st.button("🎓 Beasiswa")
    kontak_btn = st.button("📞 Kontak")

# ==================================================
# SESSION CHAT
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# TAMPILKAN CHAT
# ==================================================
for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-chat">
                <div class="user-bubble">
                    👤 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-chat">
                <div class="bot-bubble">
                    🎓 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# INPUT USER
# ==================================================
prompt = st.chat_input(
    "Tanyakan sesuatu tentang PMB Sains Data..."
)

# ==================================================
# MENU CEPAT
# ==================================================
if biaya_btn:
    prompt = "berapa biaya kuliah"

if daftar_btn:
    prompt = "cara pendaftaran"

if fasilitas_btn:
    prompt = "fasilitas kampus"

if kerja_btn:
    prompt = "prospek kerja"

if kip_btn:
    prompt = "beasiswa kipk"

if kontak_btn:
    prompt = "kontak admin"

# ==================================================
# JIKA ADA INPUT
# ==================================================
if prompt:

    pertanyaan = prompt.lower()

    # simpan chat user
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # daftar sapaan
    sapaan = [
        "halo",
        "hai",
        "hello",
        "hi",
        "assalamualaikum"
    ]

    # topik luar
    outside_topics = [
        "presiden",
        "politik",
        "anime",
        "game",
        "bola"
    ]

    with st.spinner("🤖 Sedang mencari informasi..."):

        time.sleep(1)

        # ==================================================
        # SAPAAN
        # ==================================================
        if pertanyaan in sapaan:

            response = (
                "Halo 👋 Selamat datang di Smart PMB "
                "Sains Data UPRIGSBA.\n\n"
                "Silakan tanyakan informasi mengenai "
                "biaya kuliah, pendaftaran, fasilitas, "
                "beasiswa, prospek kerja, dan lainnya."
            )

        # ==================================================
        # LUAR TOPIK
        # ==================================================
        elif any(word in pertanyaan for word in outside_topics):

            response = (
                "Maaf, chatbot ini khusus melayani "
                "informasi PMB Program Studi Sains Data."
            )

        else:

            best_score = 0
            best_answer = None

            for item in data:

                for keyword in item["keywords"]:

                    score = fuzz.ratio(
                        pertanyaan,
                        keyword.lower()
                    )

                    if score > best_score:

                        best_score = score
                        best_answer = item["jawaban"]

            # ==================================================
            # BATAS AKURASI
            # ==================================================
            if best_score >= 80:

                response = best_answer

            else:

                response = (
                    "Maaf, saya belum menemukan "
                    "informasi yang sesuai.\n\n"
                    "Silakan tanyakan informasi mengenai "
                    "PMB Program Studi Sains Data."
                )

    # simpan jawaban bot
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")

st.markdown(
    """
    <div class='footer'>
    🎓 Smart PMB Sains Data UPRIGSBA <br>
    Fakultas Sains dan Teknologi <br>
    Universitas PGRI Sumatera Barat
    </div>
    """,
    unsafe_allow_html=True
)