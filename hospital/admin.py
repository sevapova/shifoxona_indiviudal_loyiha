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
        # Data & Status
        'kasal': 'Davolanmoqda (Kasal)',
        'tuzalgan': 'Tuzalib ketgan',
        'kutilmoqda': 'Kutilmoqda',
        'yakunlandi': 'Yakunlandi',
        'bekor_qilindi': 'Bekor qilindi',
        # Disease names (Database content)
        'Oshqozon raki': 'Oshqozon raki',
        'Gripp (Influenza)': 'Gripp (Influenza)',
        'Sil (Tuberkulyoz)': 'Sil (Tuberkulyoz)',
        'Qizamiq': 'Qizamiq',
        'Gepatit B': 'Gepatit B',
        'Vabo (Cholera)': 'Vabo (Cholera)',
        'Bezgak (Malaria)': 'Bezgak (Malaria)',
        'Difteriya': 'Difteriya',
        # Page titles (singular)
        'Kasallik_s': 'Kasallik turi',
        'Shifokor_s': 'Shifokor',
        'Amaliyotchi_s': 'Amaliyotchi',
        'Bemor_s': 'Bemor',
        'Uchrashuv_s': 'Uchrashuv',
        'TibbiyYozuv_s': 'Tibbiy yozuv',
        # Field labels
        'Ism': 'Ism',
        'Familiya': 'Familiya',
        'Telefon raqami': 'Telefon raqami',
        'Yashash manzili': 'Yashash manzili',
        'Holati': 'Holati',
        'Holat': 'Holat',
        'Tavsifi': 'Tavsifi',
        'Kasallik nomi': 'Kasallik nomi',
        'Kasallik rasmi': 'Kasallik rasmi',
        'Davolaydigan kasalliklari': 'Davolaydigan kasalliklari',
        'Ish tajribasi (yil)': 'Ish tajribasi (yil)',
        'Ustoz shifokor': 'Ustoz shifokor',
        'Amaliyot boshlangan sana': 'Amaliyot boshlangan sana',
        "Tug'ilgan sana": "Tug'ilgan sana",
        'Kasalligi': 'Kasalligi',
        'Kelgan vaqti': 'Kelgan vaqti',
        'Tuzalgan vaqti': 'Tuzalgan vaqti',
        'Uchrashuv sanasi va vaqti': 'Uchrashuv sanasi va vaqti',
        'Bemor': 'Bemor',
        'Shifokor': 'Shifokor',
        'Tashxis': 'Tashxis',
        'Davolash tavsiyalari': 'Davolash tavsiyalari',
        'Yozuv sanasi': 'Yozuv sanasi',
        "Bog'liq uchrashuv": "Bog'liq uchrashuv",
        'Mutaxassisligi': 'Mutaxassisligi',
        'Rasm': 'Rasm',
        # Page headers
        'site_header': '🏥 Shifoxona Boshqaruv Tizimi',
        'site_title': 'Shifoxona Admin',
        'index_title': 'Boshqaruv paneli',
        # Fieldset titles
        "Shaxsiy ma'lumotlar": "Shaxsiy ma'lumotlar",
        "Tibbiy ma'lumotlar": "Tibbiy ma'lumotlar",
        "Kasbiy ma'lumotlar": "Kasbiy ma'lumotlar",
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
        # Data & Status
        'kasal': 'Лечится',
        'tuzalgan': 'Выздоровел',
        'kutilmoqda': 'Ожидается',
        'yakunlandi': 'Завершено',
        'bekor_qilindi': 'Отменено',
        # Disease names (Database content)
        'Oshqozon raki': 'Рак желудка',
        'Gripp (Influenza)': 'Грипп',
        'Sil (Tuberkulyoz)': 'Туберкулез',
        'Qizamiq': 'Корь',
        'Gepatit B': 'Гепатит Б',
        'Vabo (Cholera)': 'Холера',
        'Bezgak (Malaria)': 'Малярия',
        'Difteriya': 'Дифтерия',
        # Page titles (singular)
        'Kasallik_s': 'Тип болезни',
        'Shifokor_s': 'Врач',
        'Amaliyotchi_s': 'Стажер',
        'Bemor_s': 'Пациент',
        'Uchrashuv_s': 'Запись на приём',
        'TibbiyYozuv_s': 'Медицинская запись',
        # Field labels
        'Ism': 'Имя',
        'Familiya': 'Фамилия',
        'Telefon raqami': 'Номер телефона',
        'Yashash manzili': 'Адрес проживания',
        'Holati': 'Статус',
        'Holat': 'Статус',
        'Tavsifi': 'Описание',
        'Kasallik nomi': 'Название болезни',
        'Kasallik rasmi': 'Изображение',
        'Davolaydigan kasalliklari': 'Лечимые заболевания',
        'Ish tajribasi (yil)': 'Опыт работы (лет)',
        'Ustoz shifokor': 'Наставник-врач',
        'Amaliyot boshlangan sana': 'Дата начала стажировки',
        "Tug'ilgan sana": "Дата рождения",
        'Kasalligi': 'Заболевание',
        'Kelgan vaqti': 'Время поступления',
        'Tuzalgan vaqti': 'Время выздоровления',
        'Uchrashuv sanasi va vaqti': 'Дата и время приёма',
        'Bemor': 'Пациент',
        'Shifokor': 'Врач',
        'Tashxis': 'Диагноз',
        'Davolash tavsiyalari': 'Рекомендации по лечению',
        'Yozuv sanasi': 'Дата записи',
        "Bog'liq uchrashuv": "Связанный приём",
        'Mutaxassisligi': 'Специализация',
        'Rasm': 'Изображение',
        # Page headers
        'site_header': '🏥 Система Управления Больницей',
        'site_title': 'Админ Больницы',
        'index_title': 'Панель управления',
        # Fieldset titles
        "Shaxsiy ma'lumotlar": "Личные данные",
        "Tibbiy ma'lumotlar": "Медицинские данные",
        "Kasbiy ma'lumotlar": "Профессиональные данные",
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
        'kasal': 'Under Treatment',
        'tuzalgan': 'Recovered',
        'kutilmoqda': 'Pending',
        'yakunlandi': 'Completed',
        'bekor_qilindi': 'Cancelled',
        # Disease names
        'Oshqozon raki': 'Stomach cancer',
        'Gripp (Influenza)': 'Flu (Influenza)',
        'Sil (Tuberkulyoz)': 'Tuberculosis',
        'Qizamiq': 'Measles',
        'Gepatit B': 'Hepatitis B',
        'Vabo (Cholera)': 'Cholera',
        'Bezgak (Malaria)': 'Malaria',
        'Difteriya': 'Diphtheria',
        # Page titles (singular)
        'Kasallik_s': 'Disease Type',
        'Shifokor_s': 'Doctor',
        'Amaliyotchi_s': 'Intern',
        'Bemor_s': 'Patient',
        'Uchrashuv_s': 'Appointment',
        'TibbiyYozuv_s': 'Medical Record',
        # Field labels
        'Ism': 'First Name',
        'Familiya': 'Last Name',
        'Telefon raqami': 'Phone Number',
        'Yashash manzili': 'Address',
        'Holati': 'Status',
        'Holat': 'Status',
        'Tavsifi': 'Description',
        'Kasallik nomi': 'Disease Name',
        'Kasallik rasmi': 'Disease Image',
        'Davolaydigan kasalliklari': 'Treatable Diseases',
        'Ish tajribasi (yil)': 'Experience (years)',
        'Ustoz shifokor': 'Supervising Doctor',
        'Amaliyot boshlangan sana': 'Internship Start Date',
        "Tug'ilgan sana": "Date of Birth",
        'Kasalligi': 'Disease',
        'Kelgan vaqti': 'Admission Time',
        'Tuzalgan vaqti': 'Recovery Time',
        'Uchrashuv sanasi va vaqti': 'Date & Time',
        'Bemor': 'Patient',
        'Shifokor': 'Doctor',
        'Tashxis': 'Diagnosis',
        'Davolash tavsiyalari': 'Treatment Recommendations',
        'Yozuv sanasi': 'Record Date',
        "Bog'liq uchrashuv": "Related Appointment",
        'Mutaxassisligi': 'Specialization',
        'Rasm': 'Image',
        # Page headers
        'site_header': '🏥 Hospital Management System',
        'site_title': 'Hospital Admin',
        'index_title': 'Control Panel',
        # Fieldset titles
        "Shaxsiy ma'lumotlar": "Personal Info",
        "Tibbiy ma'lumotlar": "Medical Info",
        "Kasbiy ma'lumotlar": "Professional Info",
    }
}


def get_trans(text, lang=None):
    """Get translated text based on language."""
    if not lang:
        lang = (get_language() or 'uz')[:2]
    if lang in ADMIN_TRANS and str(text) in ADMIN_TRANS[lang]:
        return ADMIN_TRANS[lang][str(text)]
    return text


# ============================================================
# OVERRIDE DEFAULT ADMIN SITE get_app_list & each_context
# ============================================================
_original_get_app_list = admin.AdminSite.get_app_list
_original_each_context = admin.AdminSite.each_context

def _translated_get_app_list(self, request, app_label=None):
    app_list = _original_get_app_list(self, request, app_label)
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
    if lang in ADMIN_TRANS:
        trans = ADMIN_TRANS[lang]
        for app in app_list:
            # Translate App Name
            if app['name'] == 'Hospital': app['name'] = get_trans('Shifoxona', lang)
            if app['name'] == 'Authentication and Authorization': app['name'] = get_trans('Autentifikatsiya', lang)
            for model in app['models']:
                obj_name = model['object_name']
                if obj_name in trans:
                    model['name'] = trans[obj_name]
    return app_list

def _translated_each_context(self, request):
    context = _original_each_context(self, request)
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
    if lang in ADMIN_TRANS:
        context['site_header'] = ADMIN_TRANS[lang].get('site_header', context.get('site_header', ''))
        context['site_title'] = ADMIN_TRANS[lang].get('site_title', context.get('site_title', ''))
        context['index_title'] = ADMIN_TRANS[lang].get('index_title', context.get('index_title', ''))
    return context

admin.AdminSite.get_app_list = _translated_get_app_list
admin.AdminSite.each_context = _translated_each_context


# ============================================================
# TRANSLATED ADMIN BASE CLASS
# ============================================================
class TranslatedAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        for field_name in form.base_fields:
            label = form.base_fields[field_name].label
            if label:
                form.base_fields[field_name].label = get_trans(str(label), lang)
        return form

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        if lang in ADMIN_TRANS:
            trans = ADMIN_TRANS[lang]
            obj_name = self.model._meta.object_name
            plural = trans.get(obj_name, self.model._meta.verbose_name_plural)
            extra_context['title'] = plural
        return super().changelist_view(request, extra_context)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        translated = []
        for name, options in fieldsets:
            translated_name = get_trans(name) if name else name
            translated.append((translated_name, options))
        return translated


# ============================================================
# MODEL ADMIN REGISTRATIONS
# ============================================================
@admin.register(Kasallik)
class KasallikAdmin(TranslatedAdmin):
    list_display = ('nomi_trans', 'short_tavsifi', 'display_image')
    search_fields = ('nomi', 'tavsifi')
    readonly_fields = ('display_image',)
    list_per_page = 20

    def nomi_trans(self, obj):
        lang = getattr(self, 'current_lang', 'uz')
        return get_trans(obj.nomi, lang)
    nomi_trans.short_description = 'Kasallik nomi'

    def short_tavsifi(self, obj):
        lang = getattr(self, 'current_lang', 'uz')
        if obj.tavsifi:
            text = obj.tavsifi[:80] + '...' if len(obj.tavsifi) > 80 else obj.tavsifi
            return get_trans(text, lang)
        return '-'
    short_tavsifi.short_description = 'Tavsifi'

    def changelist_view(self, request, extra_context=None):
        self.current_lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        return super().changelist_view(request, extra_context)

    def display_image(self, obj):
        if obj.rasm:
            return mark_safe(f'<img src="{obj.rasm.url}" width="50" height="50" style="border-radius: 8px; object-fit: cover;" />')
        return "-"
    display_image.short_description = 'Rasm'


@admin.register(Bemor)
class BemorAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'telefon_raqam', 'kasalligi_trans', 'holati_trans', 'kelgan_vaqti')
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    list_filter = ('holati', 'kasalligi')
    list_per_page = 20

    def changelist_view(self, request, extra_context=None):
        self.current_lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        return super().changelist_view(request, extra_context)

    def kasalligi_trans(self, obj):
        lang = getattr(self, 'current_lang', 'uz')
        return get_trans(str(obj.kasalligi), lang) if obj.kasalligi else "-"
    kasalligi_trans.short_description = 'Kasalligi'

    def holati_trans(self, obj):
        lang = getattr(self, 'current_lang', 'uz')
        return get_trans(obj.holati, lang)
    holati_trans.short_description = 'Holati'


@admin.register(Shifokor)
class ShifokorAdmin(TranslatedAdmin):
    list_display = ('full_name', 'get_kasalliklar', 'ish_tajribasi_yillar', 'telefon_raqam')
    search_fields = ('ism', 'familiya')
    list_per_page = 20

    def changelist_view(self, request, extra_context=None):
        self.current_lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
        return super().changelist_view(request, extra_context)

    def full_name(self, obj):
        return f'Dr. {obj.ism} {obj.familiya}'
    full_name.short_description = 'Shifokor'

    def get_kasalliklar(self, obj):
        lang = getattr(self, 'current_lang', 'uz')
        return ', '.join([get_trans(k.nomi, lang) for k in obj.kasallik_yonalishlari.all()[:3]])
    get_kasalliklar.short_description = 'Mutaxassisligi'


@admin.register(Amaliyotchi)
class AmaliyotchiAdmin(TranslatedAdmin):
    list_display = ('ism', 'familiya', 'telefon_raqam', 'ustoz_shifokor', 'kelgan_sana')
    list_per_page = 20


@admin.register(Uchrashuv)
class UchrashuvAdmin(TranslatedAdmin):
    list_display = ('bemor', 'shifokor', 'sana_va_vaqt', 'holat_trans')
    list_per_page = 20

    def holat_trans(self, obj):
        return get_trans(obj.holat)
    holat_trans.short_description = 'Holat'


@admin.register(TibbiyYozuv)
class TibbiyYozuvAdmin(TranslatedAdmin):
    list_display = ('bemor', 'shifokor', 'yozuv_sanasi')
    list_per_page = 20
