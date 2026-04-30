from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import telebot
from .models import Uchrashuv, Bemor

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

@receiver(post_save, sender=Uchrashuv)
def notify_appointment(sender, instance, created, **kwargs):
    if created and bot:
        try:
            if instance.bemor.telegram_id:
                msg = f"🔔 *Yangi uchrashuv!*\n\n👨‍⚕️ Shifokor: Dr. {instance.shifokor.ism}\n🕐 Vaqt: {instance.sana_va_vaqt.strftime('%d.%m.%Y %H:%M')}"
                bot.send_message(instance.bemor.telegram_id, msg, parse_mode="Markdown")
            
            if instance.shifokor.telegram_id:
                msg = f"👨‍⚕️ *Doktor, sizda yangi qabul!*\n\n👤 Bemor: {instance.bemor.ism}\n🕐 Vaqt: {instance.sana_va_vaqt.strftime('%d.%m.%Y %H:%M')}"
                bot.send_message(instance.shifokor.telegram_id, msg, parse_mode="Markdown")
        except:
            pass

@receiver(post_save, sender=Bemor)
def notify_new_patient(sender, instance, created, **kwargs):
    if created and bot and instance.telegram_id:
        try:
            msg = f"🏥 *Xush kelibsiz!*\n\nSiz shifoxonamiz ro'yxatiga kiritildingiz.\n📱 Telefon: {instance.telefon_raqam}\n🔑 Parolingiz: {instance.parol}"
            bot.send_message(instance.telegram_id, msg, parse_mode="Markdown")
        except:
            pass
