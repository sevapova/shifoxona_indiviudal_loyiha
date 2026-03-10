from django.contrib import admin
from .models import Bemor, Shifokor, Uchrashuv, TibbiyYozuv, Kasallik, Amaliyotchi

# Admin site customization
admin.site.site_header = '🏥 Shifoxona Boshqaruv Tizimi'
admin.site.site_title = 'Shifoxona Admin'
admin.site.index_title = 'Boshqaruv paneli'


class TibbiyYozuvInline(admin.TabularInline):
    model = TibbiyYozuv
    extra = 0
    readonly_fields = ('yozuv_sanasi',)
    fields = ('shifokor', 'tashxis', 'tavsiyalar', 'uchrashuv', 'yozuv_sanasi')


class UchrashuvInline(admin.TabularInline):
    model = Uchrashuv
    extra = 0
    fk_name = 'bemor'
    fields = ('shifokor', 'sana_va_vaqt', 'holat')


@admin.register(Kasallik)
class KasallikAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'short_tavsifi', 'rasm')
    search_fields = ('nomi', 'tavsifi')
    list_per_page = 20

    def short_tavsifi(self, obj):
        if obj.tavsifi:
            return obj.tavsifi[:80] + '...' if len(obj.tavsifi) > 80 else obj.tavsifi
        return '-'
    short_tavsifi.short_description = 'Tavsifi'


@admin.register(Bemor)
class BemorAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'telefon_raqam', 'kasalligi', 'holati', 'kelgan_vaqti', 'tuzalgan_vaqti')
    search_fields = ('ism', 'familiya', 'telefon_raqam', 'manzil')
    list_filter = ('holati', 'kasalligi', 'kelgan_vaqti')
    list_editable = ('holati',)
    date_hierarchy = 'kelgan_vaqti'
    list_per_page = 20
    inlines = [UchrashuvInline, TibbiyYozuvInline]
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('ism', 'familiya', 'tugilgan_sana', 'telefon_raqam', 'manzil')
        }),
        ('Tibbiy ma\'lumotlar', {
            'fields': ('kasalligi', 'holati', 'kelgan_vaqti', 'tuzalgan_vaqti')
        }),
    )


@admin.register(Shifokor)
class ShifokorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_kasalliklar', 'ish_tajribasi_yillar', 'telefon_raqam')
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    filter_horizontal = ('kasallik_yonalishlari',)
    list_filter = ('ish_tajribasi_yillar', 'kasallik_yonalishlari')
    list_per_page = 20
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('ism', 'familiya', 'telefon_raqam', 'manzil')
        }),
        ('Kasbiy ma\'lumotlar', {
            'fields': ('kasallik_yonalishlari', 'ish_tajribasi_yillar')
        }),
    )

    def full_name(self, obj):
        return f'Dr. {obj.ism} {obj.familiya}'
    full_name.short_description = 'Shifokor'

    def get_kasalliklar(self, obj):
        return ', '.join([k.nomi for k in obj.kasallik_yonalishlari.all()[:3]])
    get_kasalliklar.short_description = 'Mutaxassisligi'


@admin.register(Amaliyotchi)
class AmaliyotchiAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'telefon_raqam', 'ustoz_shifokor', 'kelgan_sana')
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    list_filter = ('ustoz_shifokor', 'kelgan_sana')
    list_per_page = 20


@admin.register(Uchrashuv)
class UchrashuvAdmin(admin.ModelAdmin):
    list_display = ('bemor', 'shifokor', 'sana_va_vaqt', 'holat')
    list_filter = ('holat', 'sana_va_vaqt', 'shifokor')
    search_fields = ('bemor__ism', 'bemor__familiya', 'shifokor__ism', 'shifokor__familiya')
    list_editable = ('holat',)
    date_hierarchy = 'sana_va_vaqt'
    list_per_page = 20


@admin.register(TibbiyYozuv)
class TibbiyYozuvAdmin(admin.ModelAdmin):
    list_display = ('bemor', 'shifokor', 'short_tashxis', 'yozuv_sanasi')
    search_fields = ('bemor__ism', 'bemor__familiya', 'tashxis', 'tavsiyalar')
    list_filter = ('shifokor', 'yozuv_sanasi')
    readonly_fields = ('yozuv_sanasi',)
    date_hierarchy = 'yozuv_sanasi'
    list_per_page = 20

    def short_tashxis(self, obj):
        return obj.tashxis[:60] + '...' if len(obj.tashxis) > 60 else obj.tashxis
    short_tashxis.short_description = 'Tashxis'
