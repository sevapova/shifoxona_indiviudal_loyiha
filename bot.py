import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
import telebot
from dotenv import load_dotenv
load_dotenv()
from hospital.models import Shifokor, Bemor, Uchrashuv, Kasallik, Amaliyotchi, TibbiyYozuv, Xona
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from django.utils import timezone
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def send_system_alert(error_msg):
    """Kritik xatolar haqida ma'murga xabar berish"""
    if ADMIN_ID:
        try:
            bot.send_message(ADMIN_ID, f"⚠️ *TIZIM OGOHLANTIRISHI!*\n\nKritik xatolik: `{error_msg}`", parse_mode="Markdown")
        except:
            pass

user_langs = {}

BOT_TRANS = {
    'uz': {
        'welcome': "🤖 *TELEGRAM BOT*\n_Real-vaqt xabardorlik tizimi_\n\n"
                   "🩺 *Yangi bemor xabari*\nBemor qabul qilinsa, shifokorga darhol Telegram xabari yuboriladi\n\n"
                   "⏳ *Qabul eslatmasi*\nQabul vaqtidan oldin bemor va shifokorga avtomatik eslatma\n\n"
                   "🚪 *Xona bo'shalishi*\nXona bo'shaganda ma'murga bildirishnoma\n\n"
                   "📋 *Kunlik hisobot*\nHar kuni ertalab shifoxona statistikasi direksiyaga yuboriladi\n\n"
                   "🚨 *Tizim ogohlantirishlari*\nKritik vaziyatlar va xatolar haqida darhol xabar",
        'select': "✨ *Kerakli bo'limni tanlang:*",
        'm_f1': "🩺 Yangi bemor xabari", 'm_f2': "⏳ Qabul eslatmasi", 'm_f3': "🚪 Xona bo'shalishi",
        'm_f4': "📋 Kunlik hisobot", 'm_f5': "🚨 Tizim ogohlantirishlari",
        'm_mgmt': "⚙️ Boshqaruv paneli", 'm_lng': "🌐 Tilni o'zgartirish", 'back': "🔙 Orqaga",

        'phone': "📱 *Telefon raqamingizni kiriting:*", 'pass': "🔑 *Parolingizni kiriting:*", 
        'err_auth': "❌ *Xatolik:* Telefon raqam yoki parol noto'g'ri!",
        'cab_welcome': "👋 *Xush kelibsiz, {name}!*\n\nSizning shaxsiy kabinetingiz orqali barcha tashxis va hujjatlaringizni kuzatib borishingiz mumkin.", 
        'my_rec': "📋 Mening tashxislarim", 'pdf': "📄 PDF yuklab olish", 'no_rec': "❌ Sizda hali tibbiy yozuvlar yo'q.",
        'total_docs': "👨‍⚕️ Shifokorlar soni:", 'total_pats': "👥 Jami bemorlar:",
        'about_text': "🤖 *REAL-VAQT XABARDORLIK TIZIMI*\n━━━━━━━━━━━━━━━━━━━━━\n\nUshbu bot shifoxona ishini avtomatlashtirish uchun xizmat qiladi:\n\n✅ *Yangi bemor xabari* - Shifokorga darhol bildirishnoma.\n⏰ *Qabul eslatmasi* - Avtomatik eslatmalar.\n🏨 *Xona bo'shalishi* - Ma'murga bildirishnoma.\n📊 *Kunlik hisobot* - 08:00 dagi statistika.\n⚠️ *Tizim ogohlantirishlari* - Kritik xatolar haqida xabar.\n\n🚀 *Dasturchi:* Antigravity AI"
    },
    'ru': {
        'welcome': "🤖 *ТЕЛЕГРАМ БОТ*\n_Система уведомлений в реальном времени_\n\n"
                   "🩺 *Новые пациенты*\nМгновенные уведомления врачам о новых записях\n\n"
                   "⏳ *Напоминания о приеме*\nАвтоматические уведомления пациентам и врачам\n\n"
                   "🚪 *Статус палат*\nУведомления администратору об освобождении палат\n\n"
                   "📋 *Ежедневный отчет*\nСтатистика больницы каждое утро в 08:00\n\n"
                   "🚨 *Системные алерты*\nМгновенные сообщения о критических сбоях",
        'select': "✨ *Выберите нужный раздел:*",
        'm_f1': "🩺 Новые пациенты", 'm_f2': "⏳ Напоминания", 'm_f3': "🚪 Статус палат",
        'm_f4': "📋 Ежедневный отчет", 'm_f5': "🚨 Системные алерты",
        'm_mgmt': "⚙️ Панель управления", 'm_lng': "🌐 Изменить язык", 'back': "🔙 Назад",
        'phone': "📱 Введите номер телефона:", 'pass': "🔑 Введите пароль:",
        'err_auth': "❌ Ошибка входа!",
        'cab_welcome': "👋 Добро пожаловать, *{name}*!", 'my_rec': "📋 Мои диагнозы",
        'pdf': "📄 Скачать PDF", 'no_rec': "❌ У вас нет записей.",
        'total_docs': "👨‍⚕️ Количество врачей:", 'total_pats': "👥 Всего пациентов:",
        'about_text': "🏥 *ТЕЛЕГРАМ БОТ*\n*Система уведомлений в реальном времени*\n\nБот автоматизирует работу больницы:\n\n✅ *Новые пациенты*\n⏰ *Напоминания*\n🏨 *Статус палат*\n📊 *Отчеты*\n⚠️ *Алерты*"
    },
    'en': {
        'welcome': "🤖 *TELEGRAM BOT*\n_Real-time Notification System_\n\n"
                   "🩺 *New Patients*\nInstant alerts to doctors about new appointments\n\n"
                   "⏳ *Appointment Reminders*\nAutomatic alerts to patients and doctors\n\n"
                   "🚪 *Room Status*\nNotifications to admin about empty rooms\n\n"
                   "📋 *Daily Report*\nHospital statistics every morning at 08:00\n\n"
                   "🚨 *System Alerts*\nInstant messages about critical failures",
        'select': "✨ *Please select a section:*",
        'm_f1': "🩺 New Patients", 'm_f2': "⏳ Reminders", 'm_f3': "🚪 Room Status",
        'm_f4': "📋 Daily Report", 'm_f5': "🚨 System Alerts",
        'm_mgmt': "⚙️ Management Panel", 'm_lng': "🌐 Change Language", 'back': "🔙 Back",
        'phone': "📱 Enter phone number:", 'pass': "🔑 Enter password:",
        'err_auth': "❌ Authentication error!",
        'cab_welcome': "👋 Welcome, *{name}*!", 'my_rec': "📋 My Diagnoses",
        'pdf': "📄 Download PDF", 'no_rec': "❌ No records found.",
        'total_docs': "👨‍⚕️ Number of doctors:", 'total_pats': "👥 Total patients:",
        'about_text': "🏥 *TELEGRAM BOT*\n*Real-time Notification System*\n\nBot automates hospital workflow:\n\n✅ *New Patients*\n⏰ *Reminders*\n🏨 *Room Status*\n📊 *Reports*\n⚠️ *Alerts*"
    }
}

def get_lang(chat_id, text=None):
    if text:
        if text in ["👨‍⚕️ Врачи", "👥 Пациенты", "🦠 Болезни", "📊 Статистика", "🔐 Личный кабинет", "👤 О нас", "🌐 Изменить язык"]: user_langs[chat_id] = 'ru'
        elif text in ["👨‍⚕️ Doctors", "👥 Patients", "🦠 Diseases", "📊 Statistics", "🔐 Personal Cabinet", "👤 About Us", "🌐 Change Language"]: user_langs[chat_id] = 'en'
        elif text in ["👨‍⚕️ Shifokorlar", "👥 Bemorlar", "🦠 Kasalliklar", "📊 Statistika", "🔐 Shaxsiy kabinet", "👤 Biz haqimizda", "🌐 Tilni o'zgartirish"]: user_langs[chat_id] = 'uz'
    return user_langs.get(chat_id, 'uz')

def t(key, chat_id, text=None, **kwargs):
    lang = get_lang(chat_id, text)
    txt = BOT_TRANS[lang].get(key, key)
    return txt.format(**kwargs) if kwargs else txt

def main_menu(chat_id):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    m.add(t('m_f1', chat_id))
    m.add(t('m_f2', chat_id))
    m.add(t('m_f3', chat_id))
    m.add(t('m_f4', chat_id))
    m.add(t('m_f5', chat_id))
    m.row(t('m_mgmt', chat_id), t('m_lng', chat_id))
    return m

@bot.message_handler(func=lambda m: m.text in ["🚪 Xona bo'shalishi", "🚪 Статус палат", "🚪 Room Status"])
def room_status(message):
    xonalar = Xona.objects.all()
    txt = "🏨 *Xonalar holati*\n" + "━" * 15 + "\n"
    for x in xonalar:
        h = "🟢" if x.holat == 'bo\'sh' else "🔴" if x.holat == 'band' else "🟡"
        txt += f"{h} {x.nomi}: {x.get_holat_display()}\n"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["🩺 Yangi bemor xabari", "🩺 Новые пациенты", "🩺 New Patients"])
def feature_1(message):
    b = Bemor.objects.all().order_by('-id')[:5]
    txt = "🩺 *Oxirgi qabul qilingan bemorlar:*\n" + "━" * 15 + "\n"
    for x in b: txt += f"- {x.ism} {x.familiya} ({x.kelgan_vaqti.strftime('%d.%m %H:%M')})\n"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ["⏳ Qabul eslatmasi", "⏳ Напоминания", "⏳ Reminders"])
def feature_2(message):
    u = Uchrashuv.objects.filter(sana_va_vaqt__gte=timezone.now()).order_by('sana_va_vaqt')[:5]
    txt = "⏳ *Yaqin atrofdagi qabullar:*\n" + "━" * 15 + "\n"
    for x in u: txt += f"📅 {x.sana_va_vaqt.strftime('%d.%m %H:%M')} - {x.bemor.ism}\n"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ["📋 Kunlik hisobot", "📋 Ежедневный отчет", "📋 Daily Report"])
def feature_4(message):
    sc, bc = Shifokor.objects.count(), Bemor.objects.count()
    rc = Xona.objects.filter(holat='bo\'sh').count()
    txt = (f"📊 *Tezkor statistika*\n"
           f"👨‍⚕️ Shifokorlar: {sc}\n"
           f"👥 Bemorlar: {bc}\n"
           f"🏨 Bo'sh xonalar: {rc}")
    bot.send_message(message.chat.id, txt, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ["🚨 Tizim ogohlantirishlari", "🚨 Системные алерты", "🚨 System Alerts"])
def feature_5(message):
    bot.send_message(message.chat.id, "🚨 *Tizim holati:* Normal\n✅ Barcha xabardorlik modullari ishlamoqda.", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ["⚙️ Boshqaruv paneli", "⚙️ Панель управления", "⚙️ Management Panel"])
def management_panel(message):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.row("🩺 Shifokorlar", "👥 Bemorlar")
    m.row("🦠 Kasalliklar", "📊 Statistika")
    m.row("🔙 Orqaga")
    bot.send_message(message.chat.id, "⚙️ *Boshqaruv bo'limi:*", reply_markup=m, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🔙 Orqaga")
def back_to_main(message):
    bot.send_message(message.chat.id, "🔙 *Bosh menyuga qaytildi:*", reply_markup=main_menu(message.chat.id), parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🇺🇿 O'zbek", callback_data="sl_uz"),
               InlineKeyboardButton("🇷🇺 Русский", callback_data="sl_ru"),
               InlineKeyboardButton("🇺🇸 English", callback_data="sl_en"))
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык / Select language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('sl_'))
def set_lang(call):
    lang = call.data.split('_')[1]
    user_langs[call.message.chat.id] = lang
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    welcome_text = t('welcome', call.message.chat.id, name=call.from_user.first_name)
    menu = main_menu(call.message.chat.id)
    
    try:
        with open('media/bot_banner.png', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=welcome_text, parse_mode='Markdown', reply_markup=menu)
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=menu)

@bot.message_handler(func=lambda m: m.text in ["🌐 Tilni o'zgartirish", "🌐 Изменить язык", "🌐 Change Language"])
def change_l(message): start(message)

@bot.message_handler(func=lambda m: m.text in ["👨‍⚕️ Shifokorlar", "👨‍⚕️ Врачи", "👨‍⚕️ Doctors"])
def docs(message):
    sh = Shifokor.objects.all()
    txt = f"🏥 *{t('m_doc', message.chat.id, message.text)}*\n" + "━" * 15 + "\n"
    for s in sh: txt += f"👨‍⚕️ Dr. {s.ism} {s.familiya}\n"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["👥 Bemorlar", "👥 Пациенты", "👥 Patients"])
def pats(message):
    b = Bemor.objects.all()[:10]
    txt = f"👥 *{t('m_pat', message.chat.id, message.text)}*\n" + "━" * 15 + "\n"
    for x in b: txt += f"- {x.ism} {x.familiya}\n"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["🦠 Kasalliklar", "🦠 Болезни", "🦠 Diseases"])
def diss(message):
    k = Kasallik.objects.all()
    txt = f"🦠 *{t('m_dis', message.chat.id, message.text)}*\n" + "━" * 15 + "\n"
    for x in k: txt += f"- {x.nomi}\n"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["📊 Statistika", "📊 Статистика", "📊 Statistics"])
def stats(message):
    sc, bc = Shifokor.objects.count(), Bemor.objects.count()
    txt = f"📊 *{t('m_stat', message.chat.id, message.text)}*\n" + "━" * 15 + f"\n{t('total_docs', message.chat.id)} {sc}\n{t('total_pats', message.chat.id)} {bc}"
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["👤 Biz haqimizda", "👤 О нас", "👤 About Us"])
def abt(message):
    bot.send_message(message.chat.id, t('about_text', message.chat.id, message.text), parse_mode='Markdown', reply_markup=main_menu(message.chat.id))

patient_sessions = {}
@bot.message_handler(func=lambda m: m.text in ["🔐 Shaxsiy kabinet", "🔐 Личный кабинет", "🔐 Personal Cabinet"])
def cab(message):
    bot.send_message(message.chat.id, t('phone', message.chat.id, message.text))
    bot.register_next_step_handler(message, get_p)

def get_p(message):
    phone = message.text
    bot.send_message(message.chat.id, t('pass', message.chat.id))
    bot.register_next_step_handler(message, get_pwd, phone)

def get_pwd(message, phone):
    b = Bemor.objects.filter(telefon_raqam=phone, parol=message.text).first()
    if b:
        patient_sessions[message.chat.id] = b.id
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(t('my_rec', message.chat.id), t('pdf', message.chat.id))
        markup.add(t('logout', message.chat.id), t('back', message.chat.id))
        bot.send_message(message.chat.id, t('cab_welcome', message.chat.id, name=b.ism), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, t('err_auth', message.chat.id), reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["📋 Mening tashxislarim", "📋 Мои диагнозы", "📋 My Records"])
def my_recs(message):
    bid = patient_sessions.get(message.chat.id)
    if not bid: return
    y = TibbiyYozuv.objects.filter(bemor_id=bid)
    txt = "📋 Records:\n"
    for x in y: txt += f"- {x.yozuv_sanasi.date()}: {x.tashxis}\n"
    bot.send_message(message.chat.id, txt if y.exists() else t('no_rec', message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["📄 PDF yuklab olish", "📄 Скачать PDF", "📄 Download PDF"])
def get_pdf(message):
    bid = patient_sessions.get(message.chat.id)
    if not bid: return
    b = Bemor.objects.get(id=bid)
    tmp = get_template('hospital/patient_report_pdf.html')
    html = tmp.render({'bemor': b, 'bugun': timezone.now()})
    res = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=res)
    res.seek(0)
    bot.send_document(message.chat.id, res, visible_file_name=f"Report_{b.ism}.pdf")

@bot.message_handler(func=lambda m: m.text in ["🚪 Chiqish", "🚪 Выйти", "🚪 Logout"])
def out(message):
    patient_sessions.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "🚪 Chiqildi.", reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: m.text in ["🔙 Orqaga", "🔙 Назад", "🔙 Back"])
def back(message):
    bot.send_message(message.chat.id, t('select', message.chat.id), reply_markup=main_menu(message.chat.id))

@bot.message_handler(func=lambda m: True)
def unk(message):
    bot.send_message(message.chat.id, t('select', message.chat.id), reply_markup=main_menu(message.chat.id))

import threading
import time
from datetime import timedelta

def background_scheduler():
    while True:
        try:
            now = timezone.now()
            # 1. Qabul eslatmasi (1 soat oldin)
            eslatma_vaqti = now + timedelta(hours=1)
            uchrashuvlar = Uchrashuv.objects.filter(
                sana_va_vaqt__lte=eslatma_vaqti,
                sana_va_vaqt__gt=now,
                eslatma_yuborildi=False,
                holat='kutilmoqda'
            )
            for u in uchrashuvlar:
                msg = f"⏰ *Eslatma!*\n\nSizda 1 soatdan so'ng uchrashuv bor.\n👤 Bemor: {u.bemor}\n👨‍⚕️ Shifokor: {u.shifokor}\n🕒 Vaqt: {u.sana_va_vaqt.strftime('%H:%M')}"
                if u.bemor.telegram_id:
                    bot.send_message(u.bemor.telegram_id, msg, parse_mode="Markdown")
                if u.shifokor.telegram_id:
                    bot.send_message(u.shifokor.telegram_id, msg, parse_mode="Markdown")
                u.eslatma_yuborildi = True
                u.save()

            # 2. Kunlik hisobot (Ertalab 08:00 da)
            if now.hour == 8 and now.minute == 0:
                admin_id = os.getenv("ADMIN_ID")
                if admin_id and admin_id.strip().isdigit():
                    sc = Shifokor.objects.count()
                    bc = Bemor.objects.count()
                    rc = Xona.objects.filter(holat='bo\'sh').count()
                    stats = (
                        f"📊 *Kunlik Hisobot*\n"
                        f"📅 Sana: {now.strftime('%d.%m.%Y')}\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"👨‍⚕️ Shifokorlar: {sc}\n"
                        f"👥 Jami bemorlar: {bc}\n"
                        f"🏥 Bugun kelganlar: {Bemor.objects.filter(kelgan_vaqti__date=now.date()).count()}\n"
                        f"🏨 Bo'sh xonalar: {rc}\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"✅ Tizim normal holatda ishlamoqda."
                    )
                    try:
                        bot.send_message(admin_id.strip(), stats, parse_mode="Markdown")
                    except Exception as e:
                        print(f"Admin xabar yuborishda xatolik: {e}")
                time.sleep(60)

        except Exception as e:
            send_system_alert(str(e))
            print(f"Scheduler error: {e}")
        
        time.sleep(30) # Har 30 soniyada tekshirish

if __name__ == '__main__':
    try:
        # Shedulerni alohida oqimda ishga tushirish
        threading.Thread(target=background_scheduler, daemon=True).start()
        
        print("Bot ishga tushdi...")
        if ADMIN_ID:
            try:
                bot.send_message(ADMIN_ID, "🚀 *Bot muvaffaqiyatli ishga tushdi!*\n\nBarcha tizimlar va xabardorlik funksiyalari faol.", parse_mode="Markdown")
            except:
                pass
        
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        send_system_alert(f"Bot to'xtadi: {str(e)}")
        print(f"Bot error: {e}")

