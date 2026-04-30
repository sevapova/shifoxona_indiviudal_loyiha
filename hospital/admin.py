from django.contrib import admin
from django.utils.translation import gettext_lazy as _, get_language
from django.utils.safestring import mark_safe
from .models import Bemor, Shifokor, Uchrashuv, TibbiyYozuv, Kasallik, Amaliyotchi

# ============================================================
# MASTER TRANSLATION DICTIONARY (UZ / RU / EN)
# ============================================================
ADMIN_TRANS = {
    'uz': {
        # Model names (sidebar)
        'Kasallik': 'Kasallik turlari',
        'Shifokor': 'Shifokorlar',
        'Amaliyotchi': 'Amaliyotchilar',
        'Bemor': 'Bemorlar',
        'Uchrashuv': 'Uchrashuvlar',
        'TibbiyYozuv': 'Tibbiy yozuvlar',
        'Group': 'Guruhlar',
        'User': 'Foydalanuvchilar',
        'Shifoxona': 'Shifoxona',
        'Autentifikatsiya': 'Autentifikatsiya',
        # Data & Status
        'kasal': 'Davolanmoqda (Kasal)',
        'tuzalgan': 'Tuzalib ketgan',
        'kutilmoqda': 'Kutilmoqda',
        'yakunlandi': 'Yakunlandi',
        'bekor_qilindi': 'Bekor qilindi',
        # Disease names
        'Oshqozon raki': 'Oshqozon raki',
        'Gripp (Influenza)': 'Gripp (Influenza)',
        'Sil (Tuberkulyoz)': 'Sil (Tuberkulyoz)',
        'Qizamiq': 'Qizamiq',
        'Gepatit B': 'Gepatit B',
        'Vabo (Cholera)': 'Vabo (Cholera)',
        'Bezgak (Malaria)': 'Bezgak (Malaria)',
        'Difteriya': 'Difteriya',
        # Labels & Headers
        'Ism': 'Ism',
        'Familiya': 'Familiya',
        'Telefon raqami': 'Telefon raqami',
        'Kasalligi': 'Kasalligi',
        'Holati': 'Holati',
        'Holat': 'Holat',
        'Tavsifi': 'Tavsifi',
        'Kasallik nomi': 'Kasallik nomi',
        'Mutaxassisligi': 'Mutaxassisligi',
        'Ish tajribasi (yil)': 'Ish tajribasi (yil)',
        'Kelgan vaqti': 'Kelgan vaqti',
        'Rasm': 'Rasm',
        'Shifokor': 'Shifokor',
        'Bemor': 'Bemor',
        'Ustoz shifokor': 'Ustoz shifokor',
        'Kelgan sana': 'Kelgan sana',
        # Page headers
        'site_header': '🏥 Shifoxona Boshqaruv Tizimi',
        'site_title': 'Shifoxona Admin',
        'index_title': 'Boshqaruv paneli',
    },
    'ru': {
        # Model names (sidebar)
        'Kasallik': 'Типы болезней',
        'Shifokor': 'Врачи',
        'Amaliyotchi': 'Стажеры',
        'Bemor': 'Пациенты',
        'Uchrashuv': 'Записи на приём',
        'TibbiyYozuv': 'Медицинские записи',
        'Group': 'Группы',
        'User': 'Пользователи',
        'Shifoxona': 'Больница',
        'Autentifikatsiya': 'Аутентификация',
        # Data & Status
        'kasal': 'Лечится',
        'tuzalgan': 'Выздоровел',
        'kutilmoqda': 'Ожидается',
        'yakunlandi': 'Завершено',
        'bekor_qilindi': 'Отменено',
        # Disease names
        'Oshqozon raki': 'Рак желудка',
        'Gripp (Influenza)': 'Грипп',
        'Sil (Tuberkulyoz)': 'Туберкулез',
        'Qizamiq': 'Корь',
        'Gepatit B': 'Гепатит Б',
        'Vabo (Cholera)': 'Холера',
        'Bezgak (Malaria)': 'Малярия',
        'Difteriya': 'Дифтерия',
        # Labels & Headers
        'Ism': 'Имя',
        'Familiya': 'Фамилия',
        'Telefon raqami': 'Номер телефона',
        'Kasalligi': 'Заболевание',
        'Holati': 'Статус',
        'Holat': 'Статус',
        'Tavsifi': 'Описание',
        'Kasallik nomi': 'Название болезни',
        'Mutaxassisligi': 'Специализация',
        'Ish tajribasi (yil)': 'Опыт работы (лет)',
        'Kelgan vaqti': 'Время поступления',
        'Rasm': 'Изображение',
        'Shifokor': 'Врач',
        'Bemor': 'Пациент',
        'Ustoz shifokor': 'Наставник',
        'Kelgan sana': 'Дата прибытия',
        # Page headers
        'site_header': '🏥 Система Управления Больницей',
        'site_title': 'Админ Больницы',
        'index_title': 'Панель управления',
    },
    'en': {
        # Model names (sidebar)
        'Kasallik': 'Disease Types',
        'Shifokor': 'Doctors',
        'Amaliyotchi': 'Interns',
        'Bemor': 'Patients',
        'Uchrashuv': 'Appointments',
        'TibbiyYozuv': 'Medical Records',
        'Group': 'Groups',
        'User': 'Users',
        'Shifoxona': 'Hospital',
        'Autentifikatsiya': 'Authentication',
        # Data & Status
        'kasal': 'Under treatment',
        'tuzalgan': 'Recovered',
        'kutilmoqda': 'Pending',
        'yakunlandi': 'Completed',
        'bekor_qilindi': 'Cancelled',
        # Disease names
        'Oshqozon raki': 'Stomach cancer',
        'Gripp (Influenza)': 'Flu',
        'Sil (Tuberkulyoz)': 'Tuberculosis',
        'Qizamiq': 'Measles',
        'Gepatit B': 'Hepatitis B',
        'Vabo (Cholera)': 'Cholera',
        'Bezgak (Malaria)': 'Malaria',
        'Difteriya': 'Diphtheria',
        # Labels & Headers
        'Ism': 'First Name',
        'Familiya': 'Last Name',
        'Telefon raqami': 'Phone',
        'Kasalligi': 'Disease',
        'Holati': 'Status',
        'Holat': 'Status',
        'Tavsifi': 'Description',
        'Kasallik nomi': 'Disease Name',
        'Mutaxassisligi': 'Specialization',
        'Ish tajribasi (yil)': 'Experience (years)',
        'Kelgan vaqti': 'Arrival time',
        'Rasm': 'Image',
        'Shifokor': 'Doctor',
        'Bemor': 'Patient',
        'Ustoz shifokor': 'Mentor',
        'Kelgan sana': 'Join Date',
        # Page headers
        'site_header': '🏥 Hospital Management System',
        'site_title': 'Hospital Admin',
        'index_title': 'Control Panel',
    }
}

def get_trans(text, lang=None):
    if not lang:
        lang = (get_language() or 'uz')[:2]
    return ADMIN_TRANS.get(lang, ADMIN_TRANS['uz']).get(str(text), str(text))

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
        self.current_lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        admin.site.site_header = get_trans('site_header', self.current_lang)
        admin.site.site_title = get_trans('site_title', self.current_lang)
        admin.site.index_title = get_trans('index_title', self.current_lang)
        return super().changelist_view(request, extra_context)

# ============================================================
# MODELS REGISTRATION
# ============================================================
@admin.register(Kasallik)
class KasallikAdmin(TranslatedAdmin):
    list_display = ('nomi_dyn', 'tavsifi_dyn', 'rasm_dyn')
    def nomi_dyn(self, obj): return get_trans(obj.nomi, self.current_lang)
    def tavsifi_dyn(self, obj): return (obj.tavsifi[:50] + '...') if obj.tavsifi else '-'
    def rasm_dyn(self, obj):
        if obj.rasm: return mark_safe(f'<img src="{obj.rasm.url}" width="40" height="40" style="border-radius:5px"/>')
        return '-'
    
    def changelist_view(self, request, extra_context=None):
        res = super().changelist_view(request, extra_context)
        self.nomi_dyn.short_description = get_trans('Kasallik nomi', self.current_lang)
        self.tavsifi_dyn.short_description = get_trans('Tavsifi', self.current_lang)
        self.rasm_dyn.short_description = get_trans('Rasm', self.current_lang)
        return res

@admin.register(Bemor)
class BemorAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'kasalligi_dyn', 'holati_dyn', 'kelgan_vaqti')
    list_filter = ('holati', 'kasalligi')
    
    def kasalligi_dyn(self, obj): return get_trans(str(obj.kasalligi), self.current_lang) if obj.kasalligi else '-'
    def holati_dyn(self, obj): return get_trans(obj.holati, self.current_lang)
    
    def changelist_view(self, request, extra_context=None):
        res = super().changelist_view(request, extra_context)
        self.kasalligi_dyn.short_description = get_trans('Kasalligi', self.current_lang)
        self.holati_dyn.short_description = get_trans('Holati', self.current_lang)
        return res

@admin.register(Shifokor)
class ShifokorAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'mutaxassisligi_dyn', 'tajriba_dyn')
    def mutaxassisligi_dyn(self, obj): return ', '.join([get_trans(k.nomi, self.current_lang) for k in obj.kasallik_yonalishlari.all()])
    def tajriba_dyn(self, obj): return f"{obj.ish_tajribasi_yillar}"
    
    def changelist_view(self, request, extra_context=None):
        res = super().changelist_view(request, extra_context)
        self.mutaxassisligi_dyn.short_description = get_trans('Mutaxassisligi', self.current_lang)
        self.tajriba_dyn.short_description = get_trans('Ish tajribasi (yil)', self.current_lang)
        return res

@admin.register(Amaliyotchi)
class AmaliyotchiAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'ustoz_dyn', 'kelgan_sana')
    def ustoz_dyn(self, obj): return f"{obj.ustoz_shifokor}" if obj.ustoz_shifokor else '-'
    def changelist_view(self, request, extra_context=None):
        res = super().changelist_view(request, extra_context)
        self.ustoz_dyn.short_description = get_trans('Ustoz shifokor', self.current_lang)
        return res

@admin.register(Uchrashuv)
class UchrashuvAdmin(TranslatedAdmin):
    list_display = ('bemor', 'shifokor', 'sana_va_vaqt', 'holat_dyn')
    def holat_dyn(self, obj): return get_trans(obj.holat, self.current_lang)
    def changelist_view(self, request, extra_context=None):
        res = super().changelist_view(request, extra_context)
        self.holat_dyn.short_description = get_trans('Holat', self.current_lang)
        return res

@admin.register(TibbiyYozuv)
class TibbiyYozuvAdmin(TranslatedAdmin):
    list_display = ('bemor', 'shifokor', 'yozuv_sanasi')
