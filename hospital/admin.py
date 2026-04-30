from django.contrib import admin
from django.utils.translation import gettext_lazy as _, get_language
from django.utils.safestring import mark_safe
from .models import Bemor, Shifokor, Uchrashuv, TibbiyYozuv, Kasallik, Amaliyotchi

# ============================================================
# MASTER TRANSLATION DICTIONARY
# ============================================================
ADMIN_TRANS = {
    'uz': {
        'Kasallik': 'Kasallik turlari', 'Shifokor': 'Shifokorlar', 'Amaliyotchi': 'Amaliyotchilar',
        'Bemor': 'Bemorlar', 'Uchrashuv': 'Uchrashuvlar', 'TibbiyYozuv': 'Tibbiy yozuvlar',
        'Group': 'Guruhlar', 'User': 'Foydalanuvchilar', 'Shifoxona': 'Shifoxona',
        'Autentifikatsiya': 'Autentifikatsiya', 'kasal': 'Davolanmoqda', 'tuzalgan': 'Tuzalib ketgan',
        'Ism': 'Ism', 'Familiya': 'Familiya', 'Kasalligi': 'Kasalligi', 'Holati': 'Holati',
        'Tavsifi': 'Tavsifi', 'Kasallik nomi': 'Kasallik nomi', 'Mutaxassisligi': 'Mutaxassisligi',
        'Ish tajribasi (yil)': 'Ish tajribasi (yil)', 'Rasm': 'Rasm', 'Holat': 'Holat',
        'site_header': '🏥 Shifoxona Boshqaruv Tizimi', 'site_title': 'Shifoxona Admin',
        'index_title': 'Boshqaruv paneli', 'Ustoz shifokor': 'Ustoz shifokor',
    },
    'ru': {
        'Kasallik': 'Типы болезней', 'Shifokor': 'Врачи', 'Amaliyotchi': 'Стажеры',
        'Bemor': 'Пациенты', 'Uchrashuv': 'Записи на приём', 'TibbiyYozuv': 'Медицинские записи',
        'Group': 'Группы', 'User': 'Пользователи', 'Shifoxona': 'Больница',
        'Autentifikatsiya': 'Аутентификация', 'kasal': 'Лечится', 'tuzalgan': 'Выздоровел',
        'Ism': 'Имя', 'Familiya': 'Фамилия', 'Kasalligi': 'Заболевание', 'Holati': 'Статус',
        'Tavsifi': 'Описание', 'Kasallik nomi': 'Название болезни', 'Mutaxassisligi': 'Специализация',
        'Ish tajribasi (yil)': 'Опыт (лет)', 'Rasm': 'Изображение', 'Holat': 'Статус',
        'site_header': '🏥 Система Управления Больницей', 'site_title': 'Админ Больницы',
        'index_title': 'Панель управления', 'Ustoz shifokor': 'Наставник',
    },
    'en': {
        'Kasallik': 'Disease Types', 'Shifokor': 'Doctors', 'Amaliyotchi': 'Interns',
        'Bemor': 'Patients', 'Uchrashuv': 'Appointments', 'TibbiyYozuv': 'Medical Records',
        'Group': 'Groups', 'User': 'Users', 'Shifoxona': 'Hospital',
        'Autentifikatsiya': 'Authentication', 'kasal': 'In Treatment', 'tuzalgan': 'Recovered',
        'Ism': 'First Name', 'Familiya': 'Last Name', 'Kasalligi': 'Disease', 'Holati': 'Status',
        'Tavsifi': 'Description', 'Kasallik nomi': 'Disease Name', 'Mutaxassisligi': 'Specialty',
        'Ish tajribasi (yil)': 'Experience', 'Rasm': 'Image', 'Holat': 'Status',
        'site_header': '🏥 Hospital Management System', 'site_title': 'Hospital Admin',
        'index_title': 'Control Panel', 'Ustoz shifokor': 'Mentor',
    }
}

def get_trans(text, lang=None):
    if not lang:
        lang = (get_language() or 'uz')[:2]
    return ADMIN_TRANS.get(lang, ADMIN_TRANS['uz']).get(str(text), str(text))

class LazyTrans:
    def __init__(self, text): self.text = text
    def __str__(self): return get_trans(self.text)
    def __html__(self): return str(self)

# ============================================================
# OVERRIDE ADMIN SITE
# ============================================================
def _translated_get_app_list(self, request, app_label=None):
    app_list = _original_get_app_list(self, request, app_label)
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
    for app in app_list:
        if app['name'] == 'Hospital': app['name'] = get_trans('Shifoxona', lang)
        if app['name'] == 'Authentication and Authorization': app['name'] = get_trans('Autentifikatsiya', lang)
        for model in app['models']:
            name = model['object_name']
            if name in ADMIN_TRANS[lang]: model['name'] = ADMIN_TRANS[lang][name]
    return app_list

_original_get_app_list = admin.AdminSite.get_app_list
admin.AdminSite.get_app_list = _translated_get_app_list

# ============================================================
# BASE ADMIN CLASS
# ============================================================
class TranslatedAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        for field in form.base_fields:
            label = form.base_fields[field].label
            if label: form.base_fields[field].label = get_trans(label, lang)
        return form

    def changelist_view(self, request, extra_context=None):
        lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        admin.site.site_header = get_trans('site_header', lang)
        admin.site.site_title = get_trans('site_title', lang)
        admin.site.index_title = get_trans('index_title', lang)
        return super().changelist_view(request, extra_context)

# ============================================================
# MODELS REGISTRATION
# ============================================================
@admin.register(Kasallik)
class KasallikAdmin(TranslatedAdmin):
    list_display = ('nomi_dyn', 'tavsifi_dyn', 'rasm_dyn')
    def nomi_dyn(self, obj): return get_trans(obj.nomi)
    def tavsifi_dyn(self, obj): return (obj.tavsifi[:50] + '...') if obj.tavsifi else '-'
    def rasm_dyn(self, obj):
        if obj.rasm: return mark_safe(f'<img src="{obj.rasm.url}" width="40" height="40" style="border-radius:5px"/>')
        return '-'
    nomi_dyn.short_description = LazyTrans('Kasallik nomi')
    tavsifi_dyn.short_description = LazyTrans('Tavsifi')
    rasm_dyn.short_description = LazyTrans('Rasm')

@admin.register(Bemor)
class BemorAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'kasalligi_dyn', 'holati_dyn', 'kelgan_vaqti')
    list_filter = ('holati', 'kasalligi')
    def kasalligi_dyn(self, obj): return get_trans(str(obj.kasalligi)) if obj.kasalligi else '-'
    def holati_dyn(self, obj): return get_trans(obj.holati)
    kasalligi_dyn.short_description = LazyTrans('Kasalligi')
    holati_dyn.short_description = LazyTrans('Holati')

@admin.register(Shifokor)
class ShifokorAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'mutaxassisligi_dyn', 'tajriba_dyn')
    def mutaxassisligi_dyn(self, obj): return ', '.join([get_trans(k.nomi) for k in obj.kasallik_yonalishlari.all()])
    def tajriba_dyn(self, obj): return f"{obj.ish_tajribasi_yillar}"
    mutaxassisligi_dyn.short_description = LazyTrans('Mutaxassisligi')
    tajriba_dyn.short_description = LazyTrans('Ish tajribasi (yil)')

@admin.register(Amaliyotchi)
class AmaliyotchiAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'ustoz_dyn', 'kelgan_sana')
    def ustoz_dyn(self, obj): return f"{obj.ustoz_shifokor}" if obj.ustoz_shifokor else '-'
    ustoz_dyn.short_description = LazyTrans('Ustoz shifokor')

@admin.register(Uchrashuv)
class UchrashuvAdmin(TranslatedAdmin):
    list_display = ('bemor', 'shifokor', 'sana_va_vaqt', 'holat_dyn')
    def holat_dyn(self, obj): return get_trans(obj.holat)
    holat_dyn.short_description = LazyTrans('Holat')

@admin.register(TibbiyYozuv)
class TibbiyYozuvAdmin(TranslatedAdmin):
    list_display = ('bemor', 'shifokor', 'yozuv_sanasi')
