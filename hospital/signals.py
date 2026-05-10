from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import telebot
from dotenv import load_dotenv
from .models import Uchrashuv, Bemor, Xona, Shifokor

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

print(f"DEBUG: Signals loaded. Bot status: {'Active' if bot else 'Inactive'}")

@receiver(post_save, sender=Uchrashuv)
def notify_appointment(sender, instance, created, **kwargs):
    print(f"DEBUG: notify_appointment signal triggered for {instance}")
    if created and bot:
        try:
            if instance.bemor.telegram_id:
                msg = f"🔔 *Yangi uchrashuv!*\n\n👨‍⚕️ Shifokor: Dr. {instance.shifokor.ism}\n🕐 Vaqt: {instance.sana_va_vaqt.strftime('%d.%m.%Y %H:%M')}"
                bot.send_message(instance.bemor.telegram_id, msg, parse_mode="Markdown")
            
            if instance.shifokor.telegram_id:
                msg = f"👨‍⚕️ *Doktor, sizda yangi qabul!*\n\n👤 Bemor: {instance.bemor.ism} {instance.bemor.familiya}\n🕐 Vaqt: {instance.sana_va_vaqt.strftime('%d.%m.%Y %H:%M')}"
                bot.send_message(instance.shifokor.telegram_id, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Signal error: {e}")

@receiver(post_save, sender=Bemor)
def notify_patient_status(sender, instance, created, **kwargs):
    print(f"DEBUG: notify_patient_status signal triggered for {instance}")
    if not bot: return
    try:
        admin_id = os.environ.get("ADMIN_ID")
        
        if created:
            # Yangi bemor ro'yxatga olindi
            if instance.telegram_id:
                msg = f"🏥 *Xush kelibsiz!*\n\nSiz shifoxonamiz ro'yxatiga kiritildingiz.\n📱 Telefon: {instance.telefon_raqam}\n🔑 Parolingiz: {instance.parol}"
                bot.send_message(instance.telegram_id, msg, parse_mode="Markdown")
            
            # Shifokorlarga xabar berish
            if instance.kasalligi:
                docs = Shifokor.objects.filter(kasallik_yonalishlari=instance.kasalligi)
                for doc in docs:
                    if doc.telegram_id:
                        msg = f"👨‍⚕️ *Yangi bemor!*\n\n👤 Bemor: {instance.ism} {instance.familiya}\n🦠 Kasallik: {instance.kasalligi.nomi}\n\nUshbu bemor sizning yo'nalishingizga tushadi."
                        bot.send_message(doc.telegram_id, msg, parse_mode="Markdown")
            
            if admin_id:
                msg = f"🆕 *Yangi bemor ro'yxatga olindi:*\n👤 {instance.ism} {instance.familiya}\n📞 {instance.telefon_raqam}"
                bot.send_message(admin_id, msg, parse_mode="Markdown")
        
        else:
            # Holat o'zgarganda xabar berish
            if instance.holati == 'tuzalgan':
                msg = f"🎉 *Tabriklaymiz!*\n\n{instance.ism} {instance.familiya} sog'ayib, shifoxonadan javob oldi.\n💊 Salomat bo'ling!"
                if instance.telegram_id:
                    bot.send_message(instance.telegram_id, msg, parse_mode="Markdown")
                if admin_id:
                    bot.send_message(admin_id, f"✅ *Bemor sog'aydi:* {instance.ism} {instance.familiya}", parse_mode="Markdown")
    except Exception as e:
        print(f"Bemor Signal error: {e}")

@receiver(post_save, sender=Xona)
def notify_room_status(sender, instance, created, **kwargs):
    print(f"DEBUG: notify_room_status signal triggered for {instance}")
    if not bot: return
    try:
        admin_id = os.environ.get("ADMIN_ID")
        if admin_id:
            if instance.holat == 'bo\'sh':
                msg = f"🏨 *Xona bo'shadi!*\n\nXona: {instance.nomi}\nTur: {instance.tur}\n\n📢 Ma'murlar diqqatiga: Xona foydalanishga tayyor."
                bot.send_message(admin_id, msg, parse_mode="Markdown")
            elif instance.holat == 'band':
                bemor_nomi = f"{instance.bemor.ism} {instance.bemor.familiya}" if instance.bemor else "Noma'lum"
                msg = f"🏨 *Xona band qilindi!*\n\nXona: {instance.nomi}\n👤 Bemor: {bemor_nomi}\n\n✅ Tizimda qayd etildi."
                bot.send_message(admin_id, msg, parse_mode="Markdown")
    except Exception as e:
        print(f"Xona Signal error: {e}")

from .models import TibbiyYozuv
@receiver(post_save, sender=TibbiyYozuv)
def notify_medical_record(sender, instance, created, **kwargs):
    print(f"DEBUG: notify_medical_record signal triggered for {instance}")
    if created and bot:
        try:
            if instance.bemor.telegram_id:
                msg = f"📋 *Yangi tibbiy yozuv!*\n\nSizga yangi tashxis/yozuv qo'shildi.\n👨‍⚕️ Shifokor: {instance.shifokor}\n📝 Tashxis: {instance.tashxis}\n\nBatafsil ma'lumotni botdagi 'Shaxsiy kabinet' orqali olishingiz mumkin."
                bot.send_message(instance.bemor.telegram_id, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Medical Record Signal error: {e}")

