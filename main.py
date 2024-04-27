# bot telegram
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from random import randint
from io import BytesIO
# import openai
import os

# machine learning
from keras.models import load_model
import numpy as np
from keras.preprocessing import image

#fungsi untuk memulai bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # bold
    await update.message.reply_text("""
    *Selamat datang di medicalplantBot*
    medicalplantBot merupakan bot yang dapat membantu anda mengenali tanaman rimpang, tekan /info untuk informasi lebih lanjut""", parse_mode=ParseMode.MARKDOWN_V2)

# Fungsi untuk menampilkan informasi tentang bot
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Selamat datang di medicalplantBot

    Perintah yang tersedia :
    - /start untuk memulai bot
    - /info  untuk informasi mengenai bot
    - /show untuk menampilkan contoh gambar tanaman rimpang

    Panduan :
    kirim sebuah gambar yang sudah dikompresi dalam format JPG untuk mendeteksi jenis tanaman rimpang,

    Bot ini dapat mendeteksi 5 jenis tanaman rimpang yaitu :
    - Jahe (Zingiber officinale Rosc)
    - Kencur (Kaempferia galanga L)
    - Kunyit (Curcuma domestica)
    - Lengkuas (Alpinia galanga L.)
    - Temulawak (Curcuma xanthorrhiza Roxb)
                                    
    """)

# Fungsi untuk menampilkan contoh gambar tanaman rimpang
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(open('data/jahe.jpg', 'rb'))
    await update.message.reply_text("Jahe (Zingiber officinale Rosc)")
    await update.message.reply_photo(open('data/kencur.jpg', 'rb'))
    await update.message.reply_text("Kencur (Kaempferia galanga L)")
    await update.message.reply_photo(open('data/kunyit.jpg', 'rb'))
    await update.message.reply_text("Kunyit (Curcuma domestica)")
    await update.message.reply_photo(open('data/lengkuas.jpg', 'rb'))
    await update.message.reply_text("Lengkuas (Alpinia galanga L.)")
    await update.message.reply_photo(open('data/temulawak.jpg', 'rb'))
    await update.message.reply_text("Temulawak (Curcuma xanthorrhiza Roxb)")

# Fungsi untuk menyimpan gambar yang dikirim oleh pengguna dan melakukan prediksi dengan model machine learning
async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('test')
    chat_id = str(update.update_id)
    file_image = await update.message.photo[0].get_file()
    file_image = await file_image.download_as_bytearray()
    f = BytesIO(file_image)
    with open("images/"+chat_id+".jpg", "wb") as fi:
        fi.write(f.getbuffer())
    await update.message.reply_photo(open("images/"+chat_id+".jpg", "rb"))

    # load machine learning model
    model = load_model('./model/medicalplant.h5')

    # melakukan prediksi dengan model machine learning
    test_image = image.load_img("images/"+chat_id+".jpg", target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    print(result)
    if result[0][0]:
        await update.message.reply_text("*Klasifikasi :*\nTanaman JAHE\n\n*Manfaat :*\nMasuk Angin\n\n*Dosis :*\n 1 x 10 g rimpang / hari \n\n*Cara Penggunaan :*\nBahan dibakar sampai harum, memarkan, seduh dengan 1 cangkir air mendidih, diamkan,  mendidih, diamkan dapat ditambahkan gula jawa secukupnya dan diminum selagi hangat", parse_mode=ParseMode.MARKDOWN_V2)
    elif result[0][1]:
        await update.message.reply_text("*Klasifikasi :*\nTanaman KENCUR\n\n*Manfaat :*\n Terkilir\n\n*Dosis :*\n1 x 1 rimpang / hari\n\n*Cara Penggunaan :*\nBahan dihaluskan bersama beras dan air secukupnya, ditempelkan pada bagian yang sakit dan dibiarkan sampai kering", parse_mode=ParseMode.MARKDOWN_V2)
    elif result[0][2]:
        await update.message.reply_text("*Klasifikasi :*\nTanaman KUNYIT\n\n*Manfaat :*\nSakit Pinggang\n\n*Dosis :*\n1 x 9 g rimpang / hari \n\n*Cara Penggunaan :*\nBahan diparut, ditempelkan pada bagian yang sakit, dan didiamkan sampai kering", parse_mode=ParseMode.MARKDOWN_V2)
    elif result[0][3]:
        await update.message.reply_text("*Klasifikasi :*\nTanaman LENGKUAS\n\n*Manfaat :*\nPanu \n\n*Dosis :*\n13 x 1 jari rimpang / hari\n\n*Cara Penggunaan :*\nBahan dipotong miring, memarkan hingga berserabut, rendam dalam cuka, digosokkan pada bagian yang sakit", parse_mode=ParseMode.MARKDOWN_V2)
    elif result[0][4]:
        await update.message.reply_text("*Klasifikasi :* \nTanaman TEMULAWAK \n\n*Manfaat :* \nLetih Lesu \n\n*Dosis :* \n  2 x 25 g rimpang segar / hari, 1 jam sebelum makan \n\n*Cara Penggunaan :* \nBahan dihaluskan atau diiris, direbus dengan 3 gelas air hingga menjadi 1 gelas, dinginkan, saring dan diminum", parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await update.message.reply_text("Gambar tidak dapat diketahui")

# Fungsi untuk menangani pesan yang tidak diketahui
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = await update.message.reply_text(update.message.text)
    await update.message.reply_text(
        "Maaf, perintah '%s' tidak diketaui" % update.message.text)

# Fungsi utama untuk menjalankan bot    
def main() -> None:
    application = Application.builder().token("6744005884:AAGxQQvz1yilBtAEvP2FYNU771wsGn7zcBk").build()
    # command bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("show", show))
    application.add_handler(MessageHandler(filters.TEXT, unknown))

    # add Message Handler
    application.add_handler(MessageHandler(filters.PHOTO, save))

    # run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
