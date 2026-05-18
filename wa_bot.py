from flask import Flask, request
import requests
import json
from rapidfuzz import fuzz

app = Flask(__name__)

# =====================================
# TOKEN FONNTE
# =====================================
TOKEN = "JiHdijAegq6XUJgjBfXu"

# =====================================
# LOAD DATA JSON
# =====================================
try:
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        print("✅ data.json berhasil dimuat")
except Exception as e:
    data = []
    print("❌ Error load JSON:", e)

# =====================================
# MENU AWAL
# =====================================
menu_awal = """🎓 *Selamat Datang di Smart PMB Sains Data UPRIGSBA* 👋

Silakan pilih informasi:

1️⃣ Biaya Kuliah
2️⃣ Cara Pendaftaran
3️⃣ Beasiswa KIP-K
4️⃣ Fasilitas Kampus
5️⃣ Prospek Kerja
6️⃣ Visi Program Studi
7️⃣ Kontak Admin

Ketik angka atau pertanyaan langsung 😊
"""

# =====================================
# RESPON CHATBOT
# =====================================
def chatbot_response(user_message):

    if not user_message:
        return "Pesan kosong ❌"

    pertanyaan = user_message.lower().strip()

    # MENU ANGKA
    if pertanyaan == "1":
        return "💰 Biaya:\nSemester 1: 5.300.000\nSemester 2-8: 2.950.000"
    elif pertanyaan == "2":
        return "📝 Daftar di:\nhttps://pmb.upgrisba.ac.id"
    elif pertanyaan == "3":
        return "🎓 Tersedia Beasiswa KIP-K"
    elif pertanyaan == "4":
        return "🏫 Fasilitas:\nLab AI, Lab Komputer, Perpustakaan"
    elif pertanyaan == "5":
        return "💼 Prospek:\nData Scientist, AI Engineer"
    elif pertanyaan == "6":
        return "🌟 Visi: Unggul di bidang AI"
    elif pertanyaan == "7":
        return "📞 Admin:\n0813xxxxxxx"

    # SAPAAN
    if pertanyaan in ["halo", "hai", "hi", "hello", "menu"]:
        return menu_awal

    # PENCARIAN JSON
    best_score = 0
    best_answer = None

    for item in data:
        for keyword in item.get("keywords", []):
            score = fuzz.ratio(pertanyaan, keyword.lower())
            if score > best_score:
                best_score = score
                best_answer = item.get("jawaban")

    if best_score >= 80 and best_answer:
        return best_answer

    return "Maaf tidak ditemukan, ketik *menu* ya 😊"

# =====================================
# WEBHOOK (FIX TOTAL)
# =====================================
@app.route("/", methods=["GET"])
def home():
    return "Server aktif ✅", 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    print("\n🔥 ===== WEBHOOK MASUK =====")
    print("METHOD:", request.method)

    # HANDLE GET
    if request.method == "GET":
        return "Webhook aktif ✅", 200

    # HANDLE POST (WA dari Fonnte)
    try:
        # DEBUG semua kemungkinan data
        data_req = request.form.to_dict()
        if not data_req:
            data_req = request.json

        print("📥 DATA MASUK:", data_req)

        sender = data_req.get("sender")
        message = data_req.get("message")

        print("👤 Sender:", sender)
        print("💬 Message:", message)

        if not sender or not message:
            print("❌ Data tidak lengkap")
            return "No data", 200

        response_text = chatbot_response(message)
        print("🤖 Balasan:", response_text)

        res = requests.post(
            "https://api.fonnte.com/send",
            data={
                "target": sender,
                "message": response_text
            },
            headers={
                "Authorization": TOKEN
            }
        )

        print("📤 Status:", res.status_code)
        print("📤 Response:", res.text)

    except Exception as e:
        print("❌ ERROR:", e)

    return "OK", 200


# =====================================
# RUN
# =====================================
if __name__ == "__main__":
    print("🚀 Bot WhatsApp Aktif di http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)