import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
import telebot
from dotenv import load_dotenv
load_dotenv()
from hospital.models import Shifokor, Bemor, Uchrashuv, Kasallik, Amaliyotchi, TibbiyYozuv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from django.utils import timezone
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_langs = {}

BOT_TRANS = {
    'uz': {
        'welcome': "Assalomu alaykum, *{name}*! 🏥\nShifoxona boshqaruv tizimiga xush kelibsiz.",
        'select': "Iltimos, kerakli bo'limni tanlang:",
        'm_doc': "👨‍⚕️ Shifokorlar", 'm_pat': "👥 Bemorlar", 'm_dis': "🦠 Kasalliklar",
        'm_stat': "📊 Statistika", 'm_cab': "🔐 Shaxsiy kabinet", 'm_abt': "👤 Biz haqimizda",
        'm_lng': "🌐 Tilni o'zgartirish", 'back': "🔙 Orqaga", 'logout': "🚪 Chiqish",
        'phone': "📱 Telefon raqamingizni kiriting:", 'pass': "🔑 Parolingizni kiriting:", 
        'err_auth': "❌ Telefon raqam yoki parol noto'g'ri!",
        'cab_welcome': "👋 Xush kelibsiz, *{name}*!\nBu yerda siz o'z ma'lumotlaringizni ko'rishingiz mumkin.", 
        'my_rec': "📋 Mening tashxislarim", 'pdf': "📄 PDF yuklab olish", 'no_rec': "❌ Sizda hali tibbiy yozuvlar yo'q.",
        'total_docs': "👨‍⚕️ Shifokorlar soni:", 'total_pats': "👥 Jami bemorlar:",
        'about_text': "🏥 *Shifoxona Boshqaruv Tizimi*\n\nUshbu bot shifoxona ish faoliyatini avtomatlashtirish va bemorlarga qulaylik yaratish uchun xizmat qiladi. 🌸"
    },
    'ru': {
        'welcome': "Здравствуйте, *{name}*! 🏥\nДобро пожаловать в систему.",
        'select': "Выберите нужный раздел:",
        'm_doc': "👨‍⚕️ Врачи", 'm_pat': "👥 Пациенты", 'm_dis': "🦠 Болезни",
        'm_stat': "📊 Статистика", 'm_cab': "🔐 Личный кабинет", 'm_abt': "👤 О нас",
        'm_lng': "🌐 Изменить язык", 'back': "🔙 Назад", 'logout': "🚪 Выйти",
        'phone': "📱 Введите номер телефона:", 'pass': "🔑 Введите пароль:",
        'err_auth': "❌ Ошибка входа!",
        'cab_welcome': "👋 Добро пожаловать, *{name}*!", 'my_rec': "📋 Мои диагнозы",
        'pdf': "📄 Скачать PDF", 'no_rec': "❌ У вас нет записей.",
        'total_docs': "👨‍⚕️ Количество врачей:", 'total_pats': "👥 Всего пациентов:",
        'about_text': "🏥 *Система управления больницей*"
    },
    'en': {
        'welcome': "Hello, *{name}*! 🏥\nWelcome to the system.",
        'select': "Please select a section:",
        'm_doc': "👨‍⚕️ Doctors", 'm_pat': "👥 Patients", 'm_dis': "🦠 Diseases",
        'm_stat': "📊 Statistics", 'm_cab': "🔐 Personal Cabinet", 'm_abt': "👤 About Us",
        'm_lng': "🌐 Change Language", 'back': "🔙 Back", 'logout': "🚪 Logout",
        'phone': "📱 Enter your phone:", 'pass': "🔑 Enter your password:",
        'err_auth': "❌ Invalid credentials!",
        'cab_welcome': "👋 Welcome, *{name}*!", 'my_rec': "📋 My Records",
        'pdf': "📄 Download PDF", 'no_rec': "❌ No records found.",
        'total_docs': "👨‍⚕️ Doctors count:", 'total_pats': "👥 Total patients:",
        'about_text': "🏥 *Hospital Management System*"
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
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add(t('m_doc', chat_id), t('m_pat', chat_id))
    m.add(t('m_dis', chat_id), t('m_stat', chat_id))
    m.add(t('m_cab', chat_id), t('m_abt', chat_id))
    m.add(t('m_lng', chat_id))
    return m

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
    bot.send_message(call.message.chat.id, t('welcome', call.message.chat.id, name=call.from_user.first_name), parse_mode='Markdown', reply_markup=main_menu(call.message.chat.id))

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

if __name__ == '__main__':
    bot.infinity_polling()
