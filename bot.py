import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import telebot
from dotenv import load_dotenv

load_dotenv()

from hospital.models import Shifokor, Bemor, Uchrashuv, Kasallik, Amaliyotchi, TibbiyYozuv
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from django.utils import timezone
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN", "BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

# ============================================================
# MAIN MENU
# ============================================================
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🏥 Shifokorlar"),
        KeyboardButton("👥 Bemorlar"),
        KeyboardButton("🦠 Kasalliklar"),
        KeyboardButton("📅 Uchrashuvlar"),
        KeyboardButton("🧑‍⚕️ Amaliyotchilar"),
        KeyboardButton("📋 Tibbiy yozuvlar"),
        KeyboardButton("📊 Statistika"),
        KeyboardButton("➕ Bemor qo'shish"),
        KeyboardButton("📅 Uchrashuv belgilash"),
        KeyboardButton("👤 Biz haqimizda"),
    )
    return markup


# ============================================================
# /start COMMAND
# ============================================================
@bot.message_handler(commands=['start'])
def start_bot(message):
    photo_path = r"C:\Users\Sevara\.gemini\antigravity\brain\d7165c56-5580-48b0-b203-b00e881cd19c\hospital_bot_header_1773163175850.png"
    text = (
        f"Assalomu alaykum, *{message.from_user.first_name}*! 🌸\n\n"
        f"🏥 *Shifoxonani Boshqarish Tizimi* botiga xush kelibsiz.\n\n"
        f"Bu bot orqali siz:\n"
        f"• 👨‍⚕️ Shifokorlarni ko'rishingiz\n"
        f"• 👥 Bemorlarni boshqarishingiz\n"
        f"• 🦠 Kasallik turlarini ko'rishingiz\n"
        f"• 📅 Uchrashuvlar belgilashingiz\n"
        f"• 🧑‍⚕️ Amaliyotchilarni ko'rishingiz\n"
        f"• 📊 Statistikani ko'rishingiz\n\n"
        f"👩‍💻 Yaratuvchi: [@Latipova_Sevara](https://t.me/Latipova_Sevara)\n\n"
        f"Quyidagi menyudan kerakli bo'limni tanlang:"
    )
    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=text, parse_mode='Markdown', reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# /help COMMAND
# ============================================================
@bot.message_handler(commands=['help'])
def help_bot(message):
    text = (
        "📖 *Bot buyruqlari:*\n\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam ko'rsatish\n"
        "/stats - Statistika\n"
        "/doctors - Shifokorlar ro'yxati\n"
        "/patients - Bemorlar ro'yxati\n"
        "/diseases - Kasallik turlari\n\n"
        "Yoki menyudan tugmalarni bosing 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# STATISTIKA
# ============================================================
@bot.message_handler(commands=['stats'])
@bot.message_handler(func=lambda msg: msg.text == "📊 Statistika")
def show_statistics(message):
    shifokorlar = Shifokor.objects.count()
    bemorlar = Bemor.objects.count()
    kasal = Bemor.objects.filter(holati='kasal').count()
    tuzalgan = Bemor.objects.filter(holati='tuzalgan').count()
    uchrashuvlar = Uchrashuv.objects.count()
    kutilmoqda = Uchrashuv.objects.filter(holat='kutilmoqda').count()
    yakunlandi = Uchrashuv.objects.filter(holat='yakunlandi').count()
    kasalliklar = Kasallik.objects.count()
    amaliyotchilar = Amaliyotchi.objects.count()
    tibbiy_yozuvlar = TibbiyYozuv.objects.count()

    text = (
        "📊 *SHIFOXONA STATISTIKASI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👨‍⚕️ *Shifokorlar:* {shifokorlar} ta\n"
        f"🧑‍⚕️ *Amaliyotchilar:* {amaliyotchilar} ta\n"
        f"🦠 *Kasallik turlari:* {kasalliklar} ta\n\n"
        f"👥 *Jami bemorlar:* {bemorlar} ta\n"
        f"   🔴 Davolanmoqda: {kasal} ta\n"
        f"   🟢 Tuzalgan: {tuzalgan} ta\n\n"
        f"📅 *Jami uchrashuvlar:* {uchrashuvlar} ta\n"
        f"   ⏳ Kutilmoqda: {kutilmoqda} ta\n"
        f"   ✅ Yakunlangan: {yakunlandi} ta\n\n"
        f"📋 *Tibbiy yozuvlar:* {tibbiy_yozuvlar} ta\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# SHIFOKORLAR
# ============================================================
@bot.message_handler(commands=['doctors'])
@bot.message_handler(func=lambda msg: msg.text == "🏥 Shifokorlar")
def list_doctors(message):
    shifokorlar = Shifokor.objects.all().prefetch_related('kasallik_yonalishlari')
    if not shifokorlar.exists():
        bot.send_message(message.chat.id, "❌ Hozircha tizimda shifokorlar yo'q.", reply_markup=get_main_menu())
        return

    # Show first page with inline buttons
    markup = InlineKeyboardMarkup(row_width=2)
    for sh in shifokorlar[:10]:
        markup.add(InlineKeyboardButton(
            f"👨‍⚕️ Dr. {sh.ism} {sh.familiya}",
            callback_data=f"doc_{sh.id}"
        ))
    
    if shifokorlar.count() > 10:
        markup.add(InlineKeyboardButton("📋 Hammasini ko'rish", callback_data="doc_all"))

    text = (
        "🏥 *SHIFOKORLAR RO'YXATI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {shifokorlar.count()} ta shifokor\n\n"
        "Batafsil ma'lumot uchun shifokorni tanlang:"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('doc_'))
def doctor_detail(call):
    if call.data == 'doc_all':
        shifokorlar = Shifokor.objects.all().prefetch_related('kasallik_yonalishlari')
        text = "🏥 *BARCHA SHIFOKORLAR*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for sh in shifokorlar:
            kasalliklar = ", ".join([k.nomi for k in sh.kasallik_yonalishlari.all()])
            text += f"👨‍⚕️ *Dr. {sh.ism} {sh.familiya}*\n"
            text += f"⚕️ Mutaxassisligi: {kasalliklar or 'Belgilanmagan'}\n"
            text += f"📈 Tajriba: {sh.ish_tajribasi_yillar} yil\n"
            text += f"📞 Tel: {sh.telefon_raqam or 'Kiritilmagan'}\n"
            text += f"📍 Manzil: {sh.manzil or 'Kiritilmagan'}\n\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        return

    doc_id = call.data.split('_')[1]
    try:
        sh = Shifokor.objects.prefetch_related('kasallik_yonalishlari').get(id=doc_id)
        kasalliklar = ", ".join([k.nomi for k in sh.kasallik_yonalishlari.all()])
        bemor_soni = Uchrashuv.objects.filter(shifokor=sh).values('bemor').distinct().count()
        uchrashuv_soni = Uchrashuv.objects.filter(shifokor=sh).count()

        text = (
            f"👨‍⚕️ *Dr. {sh.ism} {sh.familiya}*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⚕️ *Mutaxassisligi:* {kasalliklar or 'Belgilanmagan'}\n"
            f"📈 *Tajriba:* {sh.ish_tajribasi_yillar} yil\n"
            f"📞 *Telefon:* {sh.telefon_raqam or 'Kiritilmagan'}\n"
            f"📍 *Manzil:* {sh.manzil or 'Kiritilmagan'}\n\n"
            f"👥 *Qabul qilgan bemorlar:* {bemor_soni} ta\n"
            f"📅 *Jami uchrashuvlar:* {uchrashuv_soni} ta"
        )

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data="back_doctors"))

        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)
    except Shifokor.DoesNotExist:
        bot.answer_callback_query(call.id, "Shifokor topilmadi!")


@bot.callback_query_handler(func=lambda call: call.data == 'back_doctors')
def back_to_doctors(call):
    shifokorlar = Shifokor.objects.all().prefetch_related('kasallik_yonalishlari')
    markup = InlineKeyboardMarkup(row_width=2)
    for sh in shifokorlar[:10]:
        markup.add(InlineKeyboardButton(
            f"👨‍⚕️ Dr. {sh.ism} {sh.familiya}",
            callback_data=f"doc_{sh.id}"
        ))
    text = (
        "🏥 *SHIFOKORLAR RO'YXATI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {shifokorlar.count()} ta shifokor\n\n"
        "Batafsil ma'lumot uchun shifokorni tanlang:"
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)


# ============================================================
# BEMORLAR
# ============================================================
@bot.message_handler(commands=['patients'])
@bot.message_handler(func=lambda msg: msg.text == "👥 Bemorlar")
def list_patients(message):
    bemorlar = Bemor.objects.all().order_by('-kelgan_vaqti')
    if not bemorlar.exists():
        bot.send_message(message.chat.id, "❌ Hozircha tizimda bemorlar yo'q.", reply_markup=get_main_menu())
        return

    kasal = bemorlar.filter(holati='kasal').count()
    tuzalgan = bemorlar.filter(holati='tuzalgan').count()

    markup = InlineKeyboardMarkup(row_width=1)
    for b in bemorlar[:10]:
        status = "🔴" if b.holati == 'kasal' else "🟢"
        markup.add(InlineKeyboardButton(
            f"{status} {b.ism} {b.familiya}",
            callback_data=f"pat_{b.id}"
        ))

    if bemorlar.count() > 10:
        markup.add(InlineKeyboardButton("📋 Hammasini ko'rish", callback_data="pat_all"))

    text = (
        "👥 *BEMORLAR RO'YXATI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {bemorlar.count()} ta bemor\n"
        f"🔴 Davolanmoqda: {kasal} ta\n"
        f"🟢 Tuzalgan: {tuzalgan} ta\n\n"
        "Batafsil ma'lumot uchun bemorni tanlang:"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('pat_'))
def patient_detail(call):
    if call.data == 'pat_all':
        bemorlar = Bemor.objects.all().order_by('-kelgan_vaqti')
        text = "👥 *BARCHA BEMORLAR*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for b in bemorlar:
            status = "🔴 Davolanmoqda" if b.holati == 'kasal' else "🟢 Tuzalgan"
            text += f"{'🔴' if b.holati == 'kasal' else '🟢'} *{b.ism} {b.familiya}*\n"
            text += f"   📞 {b.telefon_raqam or '-'} | {status}\n"
            text += f"   🦠 {b.kasalligi.nomi if b.kasalligi else 'Noaniq'}\n\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        return

    pat_id = call.data.split('_')[1]
    try:
        b = Bemor.objects.select_related('kasalligi').get(id=pat_id)
        uchrashuvlar = Uchrashuv.objects.filter(bemor=b).select_related('shifokor').order_by('-sana_va_vaqt')[:5]
        yozuvlar = TibbiyYozuv.objects.filter(bemor=b).order_by('-yozuv_sanasi')[:3]
        
        status = "🔴 Davolanmoqda" if b.holati == 'kasal' else "🟢 Tuzalgan"

        text = (
            f"👤 *{b.ism} {b.familiya}*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📞 *Telefon:* {b.telefon_raqam or 'Kiritilmagan'}\n"
            f"🎂 *Tug'ilgan sana:* {b.tugilgan_sana.strftime('%d.%m.%Y') if b.tugilgan_sana else 'Kiritilmagan'}\n"
            f"📍 *Manzil:* {b.manzil or 'Kiritilmagan'}\n"
            f"🦠 *Kasalligi:* {b.kasalligi.nomi if b.kasalligi else 'Noaniq'}\n"
            f"📌 *Holati:* {status}\n"
            f"📅 *Kelgan vaqti:* {b.kelgan_vaqti.strftime('%d.%m.%Y %H:%M')}\n"
        )

        if b.tuzalgan_vaqti:
            text += f"✅ *Tuzalgan vaqti:* {b.tuzalgan_vaqti.strftime('%d.%m.%Y %H:%M')}\n"

        if uchrashuvlar.exists():
            text += "\n📅 *So'nggi uchrashuvlar:*\n"
            for u in uchrashuvlar:
                h_icon = "⏳" if u.holat == 'kutilmoqda' else ("✅" if u.holat == 'yakunlandi' else "❌")
                text += f"  {h_icon} Dr. {u.shifokor.ism} - {u.sana_va_vaqt.strftime('%d.%m.%Y %H:%M')}\n"

        if yozuvlar.exists():
            text += "\n📋 *So'nggi tashxislar:*\n"
            for y in yozuvlar:
                text += f"  📝 {y.tashxis[:50]}... ({y.yozuv_sanasi.strftime('%d.%m.%Y')})\n"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data="back_patients"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)
    except Bemor.DoesNotExist:
        bot.answer_callback_query(call.id, "Bemor topilmadi!")


@bot.callback_query_handler(func=lambda call: call.data == 'back_patients')
def back_to_patients(call):
    bemorlar = Bemor.objects.all().order_by('-kelgan_vaqti')
    markup = InlineKeyboardMarkup(row_width=1)
    for b in bemorlar[:10]:
        status = "🔴" if b.holati == 'kasal' else "🟢"
        markup.add(InlineKeyboardButton(f"{status} {b.ism} {b.familiya}", callback_data=f"pat_{b.id}"))
    text = (
        "👥 *BEMORLAR RO'YXATI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {bemorlar.count()} ta bemor\n"
        "Batafsil ma'lumot uchun bemorni tanlang:"
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)


# ============================================================
# KASALLIKLAR
# ============================================================
@bot.message_handler(commands=['diseases'])
@bot.message_handler(func=lambda msg: msg.text == "🦠 Kasalliklar")
def list_diseases(message):
    kasalliklar = Kasallik.objects.all()
    if not kasalliklar.exists():
        bot.send_message(message.chat.id, "❌ Hozircha tizimda kasallik turlari yo'q.", reply_markup=get_main_menu())
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for k in kasalliklar:
        bemor_soni = Bemor.objects.filter(kasalligi=k).count()
        markup.add(InlineKeyboardButton(
            f"🦠 {k.nomi} ({bemor_soni} bemor)",
            callback_data=f"dis_{k.id}"
        ))

    text = (
        "🦠 *KASALLIK TURLARI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {kasalliklar.count()} ta kasallik turi\n\n"
        "Batafsil ma'lumot uchun tanlang:"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('dis_'))
def disease_detail(call):
    dis_id = call.data.split('_')[1]
    try:
        k = Kasallik.objects.get(id=dis_id)
        bemorlar = Bemor.objects.filter(kasalligi=k)
        kasal = bemorlar.filter(holati='kasal').count()
        tuzalgan = bemorlar.filter(holati='tuzalgan').count()
        shifokorlar = Shifokor.objects.filter(kasallik_yonalishlari=k)

        text = (
            f"🦠 *{k.nomi}*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📝 *Tavsifi:*\n{k.tavsifi or 'Tavsif kiritilmagan'}\n\n"
            f"👥 *Jami bemorlar:* {bemorlar.count()} ta\n"
            f"   🔴 Davolanmoqda: {kasal} ta\n"
            f"   🟢 Tuzalgan: {tuzalgan} ta\n\n"
        )

        if shifokorlar.exists():
            text += "👨‍⚕️ *Mutaxassis shifokorlar:*\n"
            for sh in shifokorlar:
                text += f"  • Dr. {sh.ism} {sh.familiya} ({sh.ish_tajribasi_yillar} yil tajriba)\n"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data="back_diseases"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)
    except Kasallik.DoesNotExist:
        bot.answer_callback_query(call.id, "Kasallik topilmadi!")


@bot.callback_query_handler(func=lambda call: call.data == 'back_diseases')
def back_to_diseases(call):
    kasalliklar = Kasallik.objects.all()
    markup = InlineKeyboardMarkup(row_width=1)
    for k in kasalliklar:
        bemor_soni = Bemor.objects.filter(kasalligi=k).count()
        markup.add(InlineKeyboardButton(f"🦠 {k.nomi} ({bemor_soni} bemor)", callback_data=f"dis_{k.id}"))
    text = (
        "🦠 *KASALLIK TURLARI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {kasalliklar.count()} ta kasallik turi\n\n"
        "Batafsil ma'lumot uchun tanlang:"
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=markup)


# ============================================================
# UCHRASHUVLAR
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == "📅 Uchrashuvlar")
def list_appointments(message):
    uchrashuvlar = Uchrashuv.objects.all().select_related('bemor', 'shifokor').order_by('-sana_va_vaqt')
    if not uchrashuvlar.exists():
        bot.send_message(message.chat.id, "❌ Hozircha belgilangan uchrashuvlar yo'q.", reply_markup=get_main_menu())
        return

    kutilmoqda = uchrashuvlar.filter(holat='kutilmoqda')
    yakunlandi = uchrashuvlar.filter(holat='yakunlandi')

    text = (
        "📅 *UCHRASHUVLAR*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {uchrashuvlar.count()} ta\n"
        f"⏳ Kutilmoqda: {kutilmoqda.count()} ta\n"
        f"✅ Yakunlangan: {yakunlandi.count()} ta\n\n"
    )

    if kutilmoqda.exists():
        text += "*⏳ Kutilayotgan uchrashuvlar:*\n"
        for u in kutilmoqda[:10]:
            text += (
                f"  📌 *{u.bemor.ism} {u.bemor.familiya}*\n"
                f"     👨‍⚕️ Dr. {u.shifokor.ism} {u.shifokor.familiya}\n"
                f"     🕐 {u.sana_va_vaqt.strftime('%d.%m.%Y %H:%M')}\n\n"
            )

    if yakunlandi.exists():
        text += "*✅ So'nggi yakunlangan:*\n"
        for u in yakunlandi[:5]:
            text += (
                f"  ✔️ {u.bemor.ism} - Dr. {u.shifokor.ism} "
                f"({u.sana_va_vaqt.strftime('%d.%m.%Y')})\n"
            )

    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# AMALIYOTCHILAR
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == "🧑‍⚕️ Amaliyotchilar")
def list_interns(message):
    amaliyotchilar = Amaliyotchi.objects.all().select_related('ustoz_shifokor')
    if not amaliyotchilar.exists():
        bot.send_message(message.chat.id, "❌ Hozircha tizimda amaliyotchilar yo'q.", reply_markup=get_main_menu())
        return

    text = (
        "🧑‍⚕️ *AMALIYOTCHILAR*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {amaliyotchilar.count()} ta amaliyotchi\n\n"
    )

    for a in amaliyotchilar:
        ustoz = f"Dr. {a.ustoz_shifokor.ism} {a.ustoz_shifokor.familiya}" if a.ustoz_shifokor else "Tayinlanmagan"
        text += (
            f"🧑‍⚕️ *{a.ism} {a.familiya}*\n"
            f"   📞 Tel: {a.telefon_raqam}\n"
            f"   📍 Manzil: {a.manzil}\n"
            f"   👨‍⚕️ Ustoz: {ustoz}\n"
            f"   📅 Boshlangan: {a.kelgan_sana.strftime('%d.%m.%Y') if a.kelgan_sana else '-'}\n\n"
        )

    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# TIBBIY YOZUVLAR
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == "📋 Tibbiy yozuvlar")
def list_medical_records(message):
    yozuvlar = TibbiyYozuv.objects.all().select_related('bemor', 'shifokor').order_by('-yozuv_sanasi')
    if not yozuvlar.exists():
        bot.send_message(message.chat.id, "❌ Hozircha tibbiy yozuvlar yo'q.", reply_markup=get_main_menu())
        return

    text = (
        "📋 *TIBBIY YOZUVLAR*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Jami: {yozuvlar.count()} ta yozuv\n\n"
    )

    for y in yozuvlar[:10]:
        text += (
            f"📝 *{y.bemor.ism} {y.bemor.familiya}*\n"
            f"   👨‍⚕️ Dr. {y.shifokor.ism if y.shifokor else 'Noaniq'}\n"
            f"   🔬 Tashxis: {y.tashxis[:60]}{'...' if len(y.tashxis) > 60 else ''}\n"
            f"   💊 Tavsiya: {y.tavsiyalar[:60] + '...' if y.tavsiyalar and len(y.tavsiyalar) > 60 else (y.tavsiyalar or 'Yo`q')}\n"
            f"   📅 Sana: {y.yozuv_sanasi.strftime('%d.%m.%Y')}\n\n"
        )

    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# BEMOR QO'SHISH (Step by step)
# ============================================================
user_data = {}

@bot.message_handler(func=lambda msg: msg.text == "➕ Bemor qo'shish")
def add_patient_start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "👤 *Yangi bemor qo'shish*\n\nBemor *ismini* kiriting:", 
                     parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_patient_name)

def get_patient_name(message):
    if message.text in ["🔙 Bekor qilish", "/start"]:
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=get_main_menu())
        return
    user_data[message.chat.id]['ism'] = message.text
    bot.send_message(message.chat.id, "Bemor *familiyasini* kiriting:", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_patient_surname)

def get_patient_surname(message):
    if message.text in ["🔙 Bekor qilish", "/start"]:
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=get_main_menu())
        return
    user_data[message.chat.id]['familiya'] = message.text
    bot.send_message(message.chat.id, "📞 *Telefon raqamini* kiriting (masalan: +998901234567):", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_patient_phone)

def get_patient_phone(message):
    if message.text in ["🔙 Bekor qilish", "/start"]:
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=get_main_menu())
        return
    user_data[message.chat.id]['telefon'] = message.text
    bot.send_message(message.chat.id, "📍 *Yashash manzilini* kiriting:", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_patient_address)

def get_patient_address(message):
    if message.text in ["🔙 Bekor qilish", "/start"]:
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=get_main_menu())
        return
    user_data[message.chat.id]['manzil'] = message.text

    # Show diseases to pick
    kasalliklar = Kasallik.objects.all()
    if kasalliklar.exists():
        markup = InlineKeyboardMarkup(row_width=1)
        for k in kasalliklar:
            markup.add(InlineKeyboardButton(f"🦠 {k.nomi}", callback_data=f"addpat_dis_{k.id}"))
        markup.add(InlineKeyboardButton("❓ Noaniq / Boshqa", callback_data="addpat_dis_0"))
        bot.send_message(message.chat.id, "🦠 *Kasallik turini* tanlang:", parse_mode='Markdown', reply_markup=markup)
    else:
        user_data[message.chat.id]['kasallik_id'] = None
        save_patient(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('addpat_dis_'))
def select_disease_for_patient(call):
    dis_id = call.data.split('_')[-1]
    user_data[call.message.chat.id]['kasallik_id'] = int(dis_id) if dis_id != '0' else None
    bot.delete_message(call.message.chat.id, call.message.message_id)
    save_patient(call.message.chat.id)


def save_patient(chat_id):
    data = user_data.get(chat_id, {})
    try:
        kasallik = None
        if data.get('kasallik_id'):
            kasallik = Kasallik.objects.get(id=data['kasallik_id'])

        bemor = Bemor.objects.create(
            ism=data['ism'],
            familiya=data['familiya'],
            telefon_raqam=data['telefon'],
            manzil=data['manzil'],
            kasalligi=kasallik,
            holati='kasal',
        )
        text = (
            f"✅ *Bemor muvaffaqiyatli qo'shildi!*\n\n"
            f"👤 {bemor.ism} {bemor.familiya}\n"
            f"📞 {bemor.telefon_raqam}\n"
            f"📍 {bemor.manzil}\n"
            f"🦠 {kasallik.nomi if kasallik else 'Noaniq'}\n"
            f"📅 {bemor.kelgan_vaqti.strftime('%d.%m.%Y %H:%M')}"
        )
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=get_main_menu())
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xatolik yuz berdi: {str(e)}", reply_markup=get_main_menu())
    
    if chat_id in user_data:
        del user_data[chat_id]


# ============================================================
# UCHRASHUV BELGILASH (Step by step)
# ============================================================
appointment_data = {}

@bot.message_handler(func=lambda msg: msg.text == "📅 Uchrashuv belgilash")
def add_appointment_start(message):
    bemorlar = Bemor.objects.filter(holati='kasal')
    if not bemorlar.exists():
        bot.send_message(message.chat.id, "❌ Davolanayotgan bemorlar yo'q.", reply_markup=get_main_menu())
        return

    appointment_data[message.chat.id] = {}
    markup = InlineKeyboardMarkup(row_width=1)
    for b in bemorlar[:15]:
        markup.add(InlineKeyboardButton(
            f"👤 {b.ism} {b.familiya}",
            callback_data=f"appt_pat_{b.id}"
        ))
    
    bot.send_message(message.chat.id, "📅 *Uchrashuv belgilash*\n\n*Bemorni* tanlang:", 
                     parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('appt_pat_'))
def select_patient_for_appt(call):
    pat_id = call.data.split('_')[-1]
    appointment_data[call.message.chat.id] = {'bemor_id': int(pat_id)}
    
    shifokorlar = Shifokor.objects.all()
    markup = InlineKeyboardMarkup(row_width=1)
    for sh in shifokorlar[:15]:
        markup.add(InlineKeyboardButton(
            f"👨‍⚕️ Dr. {sh.ism} {sh.familiya}",
            callback_data=f"appt_doc_{sh.id}"
        ))
    
    bot.edit_message_text("📅 *Uchrashuv belgilash*\n\n*Shifokorni* tanlang:", 
                         call.message.chat.id, call.message.message_id,
                         parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('appt_doc_'))
def select_doctor_for_appt(call):
    doc_id = call.data.split('_')[-1]
    appointment_data[call.message.chat.id]['shifokor_id'] = int(doc_id)
    
    bot.edit_message_text(
        "📅 *Uchrashuv belgilash*\n\n"
        "🕐 *Sana va vaqtni* kiriting\n"
        "Format: `KK.OO.YYYY SS:DD`\n"
        "Masalan: `15.03.2026 14:30`",
        call.message.chat.id, call.message.message_id,
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(call.message, get_appointment_datetime)


def get_appointment_datetime(message):
    if message.text in ["/start"]:
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=get_main_menu())
        return

    try:
        dt = datetime.strptime(message.text.strip(), '%d.%m.%Y %H:%M')
        data = appointment_data.get(message.chat.id, {})
        
        bemor = Bemor.objects.get(id=data['bemor_id'])
        shifokor = Shifokor.objects.get(id=data['shifokor_id'])
        
        uchrashuv = Uchrashuv.objects.create(
            bemor=bemor,
            shifokor=shifokor,
            sana_va_vaqt=timezone.make_aware(dt),
            holat='kutilmoqda'
        )

        text = (
            f"✅ *Uchrashuv muvaffaqiyatli belgilandi!*\n\n"
            f"👤 Bemor: {bemor.ism} {bemor.familiya}\n"
            f"👨‍⚕️ Shifokor: Dr. {shifokor.ism} {shifokor.familiya}\n"
            f"🕐 Vaqt: {dt.strftime('%d.%m.%Y %H:%M')}\n"
            f"📌 Holat: ⏳ Kutilmoqda"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())
    except ValueError:
        bot.send_message(message.chat.id, 
                        "❌ Noto'g'ri format! Iltimos, `KK.OO.YYYY SS:DD` formatida kiriting.\nMasalan: `15.03.2026 14:30`",
                        parse_mode='Markdown', reply_markup=get_main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik: {str(e)}", reply_markup=get_main_menu())

    if message.chat.id in appointment_data:
        del appointment_data[message.chat.id]


# ============================================================
# BIZ HAQIMIZDA
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == "👤 Biz haqimizda")
def about_us(message):
    text = (
        "🏥 *Shifoxonani Boshqarish Tizimi*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 *Loyiha maqsadi:*\n"
        "Bemorlar, shifokorlar va tibbiy uchrashuvlarni\n"
        "samarali boshqarish, ro'yxatga olish jarayonini\n"
        "to'liq raqamlashtirish.\n\n"
        "🔧 *Imkoniyatlar:*\n"
        "• Shifokorlar va bemorlarni boshqarish\n"
        "• Kasallik turlarini ro'yxatga olish\n"
        "• Uchrashuvlar tizimi\n"
        "• Tibbiy yozuvlar\n"
        "• Amaliyotchilar boshqaruvi\n"
        "• Statistika va hisobotlar\n\n"
        "🛠 *Texnologiyalar:*\n"
        "• Backend: Django (Python)\n"
        "• Database: PostgreSQL\n"
        "• Bot: Telegram Bot API\n"
        "• Frontend: HTML/CSS Glassmorphism\n\n"
        "👩‍💻 *Yaratuvchi:*\n"
        "[@Latipova\\_Sevara](https://t.me/Latipova_Sevara)\n\n"
        "Barcha savollar va takliflar bo'yicha\n"
        "murojaat qilishingiz mumkin. 🌸"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=get_main_menu())


# ============================================================
# UNKNOWN MESSAGES
# ============================================================
@bot.message_handler(func=lambda msg: True)
def unknown_message(message):
    bot.send_message(
        message.chat.id, 
        "🤔 Tushunmadim. Iltimos, menyudan tanlang yoki /help buyrug'ini bosing.",
        reply_markup=get_main_menu()
    )


# ============================================================
# RUN BOT
# ============================================================
if __name__ == '__main__':
    print("Shifoxona Bot ishga tushdi...")
    print("Barcha xususiyatlar faol")
    print("Telegram: @Latipova_Sevara")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
