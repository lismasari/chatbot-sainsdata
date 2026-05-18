from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

from rapidfuzz import fuzz
import json

# =========================================
# TOKEN BOT TELEGRAM
# =========================================
TOKEN = "8605842813:AAEmUEQ1BdMgg4BCz7ZPaJciwYEdCdcJGzM"

# =========================================
# LOAD DATA JSON
# =========================================
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# =========================================
# MENU BUTTON
# =========================================
keyboard = [
    ["📌 Biaya Kuliah", "📝 Cara Pendaftaran"],
    ["🎓 Profil Lulusan", "🏫 Fasilitas"],
    ["🎯 Visi Misi", "🎁 Beasiswa"],
    ["📅 Jadwal", "📞 Contact"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

# =========================================
# START COMMAND
# =========================================
def start(update: Update, context: CallbackContext):

    pesan = """
🎓 Selamat Datang di Chatbot PMB
Program Studi Sains Data UPGRISBA 👋

Silakan tanyakan informasi mengenai:

✅ Biaya Kuliah
✅ Cara Pendaftaran
✅ Beasiswa
✅ Fasilitas Kampus
✅ Profil Lulusan
✅ Visi dan Misi
✅ Jadwal Pendaftaran
✅ Contact Person

Gunakan menu di bawah atau ketik pertanyaan langsung 😊
"""

    update.message.reply_text(
        pesan,
        reply_markup=reply_markup
    )

# =========================================
# FUNGSI CARI JAWABAN
# =========================================
def cari_jawaban(user_text):

    user_text = user_text.lower()

    skor_tertinggi = 0
    jawaban_terbaik = None

    for item in data:

        for keyword in item["keywords"]:

            skor = fuzz.partial_ratio(
                user_text,
                keyword.lower()
            )

            if skor > skor_tertinggi:

                skor_tertinggi = skor
                jawaban_terbaik = item["jawaban"]

    if skor_tertinggi >= 70:
        return jawaban_terbaik

    return (
        "Maaf 😅\n\n"
        "Informasi belum ditemukan.\n\n"
        "Silakan gunakan kata kunci seperti:\n"
        "• biaya kuliah\n"
        "• fasilitas\n"
        "• visi misi\n"
        "• beasiswa\n"
        "• profil lulusan"
    )

# =========================================
# HANDLE CHAT
# =========================================
def handle_message(update: Update, context: CallbackContext):

    text = update.message.text.lower().strip()

    print("Pesan masuk:", text)

    # =====================================
    # MENU BUTTON
    # =====================================

    if "biaya" in text:
        text = "biaya kuliah"

    elif "pendaftaran" in text or "daftar" in text:
        text = "cara pendaftaran"

    elif "profil" in text:
        text = "profil lulusan"

    elif "fasilitas" in text:
        text = "fasilitas"

    elif "visi" in text or "misi" in text:
        text = "visi misi"

    elif "beasiswa" in text:
        text = "beasiswa"

    elif "jadwal" in text:
        text = "jadwal pendaftaran"

    elif "contact" in text or "kontak" in text:
        text = "contact person"

    # =====================================
    # SAPAAN
    # =====================================

    sapaan = [
        "hai",
        "halo",
        "hallo",
        "hello",
        "assalamualaikum",
        "p"
    ]

    if text in sapaan:

        update.message.reply_text(
            "Halo 👋\n\n"
            "Selamat datang di Chatbot PMB "
            "Program Studi Sains Data UPGRISBA 😊",
            reply_markup=reply_markup
        )

        return

    # =====================================
    # CARI JAWABAN
    # =====================================

    jawaban = cari_jawaban(text)

    print("Jawaban:", jawaban)

    update.message.reply_text(
        jawaban,
        reply_markup=reply_markup
    )

# =========================================
# ERROR HANDLER
# =========================================
def error(update, context):

    print(f"Terjadi error: {context.error}")

# =========================================
# MAIN
# =========================================
def main():

    updater = Updater(
        TOKEN,
        use_context=True
    )

    dp = updater.dispatcher

    # START
    dp.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # SEMUA CHAT
    dp.add_handler(
        MessageHandler(
            Filters.text,
            handle_message
        )
    )

    # ERROR
    dp.add_error_handler(error)

    print("Bot Telegram berjalan...")

    # JALANKAN BOT
    updater.start_polling(
        poll_interval=1.0,
        timeout=20
    )

    updater.idle()

# =========================================
# RUN PROGRAM
# =========================================
if __name__ == "__main__":
    main()