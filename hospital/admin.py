import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Kasallik, Shifokor, Bemor, Uchrashuv, Amaliyotchi, TibbiyYozuv, Retsept, Xona, XonaTuri

@admin.register(XonaTuri)
class XonaTuriAdmin(admin.ModelAdmin):
    list_display = ('nomi',)

@admin.register(Xona)
class XonaAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'tur', 'bemor', 'holat', 'oxirgi_tozalash')
    list_filter = ('holat', 'tur')
    search_fields = ('nomi', 'bemor__ism')



def export_shifokorlar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shifokorlar.csv"'
    writer = csv.writer(response)
    writer.writerow(['Ism', 'Familiya', 'Mutaxassislik', 'Tajriba (yil)', 'Telefon'])
    for s in queryset:
        writer.writerow([s.ism, s.familiya, s.mutaxassislik, s.ish_tajribasi_yillar, s.telefon_raqam])
    return response
export_shifokorlar_csv.short_description = "Tanlangan shifokorlarni Excelga (CSV) yuklash"

def export_bemorlar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bemorlar.csv"'
    writer = csv.writer(response)
    writer.writerow(['Ism', 'Familiya', 'Telefon', 'Holati', 'Kelgan vaqti'])
    for b in queryset:
        writer.writerow([b.ism, b.familiya, b.telefon_raqam, b.holati, b.kelgan_vaqti])
    return response
export_bemorlar_csv.short_description = "Tanlangan bemorlarni Excelga (CSV) yuklash"

@admin.register(Kasallik)
class KasallikAdmin(admin.ModelAdmin):
    list_display = ('display_nomi', 'tavsifi')
    search_fields = ('nomi',)

    def display_nomi(self, obj):
        return format_html('<span style="color: #059669; font-weight: bold;">🦠 {}</span>', obj.nomi)
    display_nomi.short_description = "Kasallik nomi"

@admin.register(Shifokor)
class ShifokorAdmin(admin.ModelAdmin):
    list_display = ('display_ism', 'display_familiya', 'mutaxassislik', 'ish_tajribasi_yillar', 'display_kasalliklar', 'telefon_raqam', 'download_report')
    list_filter = ('kasallik_yonalishlari',)
    filter_horizontal = ('kasallik_yonalishlari',)
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    actions = [export_shifokorlar_csv]

    def display_ism(self, obj):
        return format_html('<span style="color: #2563eb; font-weight: bold;">👨‍⚕️ {}</span>', obj.ism)
    display_ism.short_description = "Ismi"

    def display_familiya(self, obj):
        return format_html('<span style="color: #2563eb; font-weight: bold;">{}</span>', obj.familiya)
    display_familiya.short_description = "Familiyasi"

    def display_kasalliklar(self, obj):
        items = obj.kasallik_yonalishlari.all()
        return format_html('<div style="max-width: 200px;">{}</div>', 
                           format_html(", ".join(['<span style="color: #059669;">{}</span>'.format(k.nomi) for k in items])))
    display_kasalliklar.short_description = 'Davolaydigan kasalliklari'

    def download_report(self, obj):
        url = reverse('hospital:doctor_pdf', args=[obj.pk])
        return format_html('<a class="button" href="{}" style="background:#f06292; color:white; padding:5px 10px; border-radius:5px; text-decoration:none;">📄 Hisobot</a>', url)
    download_report.short_description = 'PDF Hisobot'

@admin.register(Bemor)
class BemorAdmin(admin.ModelAdmin):
    list_display = ('display_ism', 'familiya', 'telefon_raqam', 'display_kasallik', 'holati', 'kelgan_vaqti', 'download_report')
    list_filter = ('holati', 'kasalligi', 'kelgan_vaqti')
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    date_hierarchy = 'kelgan_vaqti'
    actions = [export_bemorlar_csv]

    def display_ism(self, obj):
        return format_html('<span style="color: #db2777; font-weight: bold;">👥 {}</span>', obj.ism)
    display_ism.short_description = "Bemor"

    def display_kasallik(self, obj):
        if obj.kasalligi:
            return format_html('<span style="color: #059669; font-weight: bold;">🦠 {}</span>', obj.kasalligi.nomi)
        return "-"
    display_kasallik.short_description = "Kasalligi"

    def download_report(self, obj):
        url = reverse('hospital:patient_pdf', args=[obj.pk])
        return format_html('<a class="button" href="{}" style="background:#2196f3; color:white; padding:5px 10px; border-radius:5px; text-decoration:none;">📄 Hisobot</a>', url)
    download_report.short_description = 'PDF Hisobot'

@admin.register(Retsept)
class RetseptAdmin(admin.ModelAdmin):
    list_display = ('bemor', 'shifokor', 'dori_nomi', 'sana')
    list_filter = ('sana', 'shifokor')
    search_fields = ('bemor__ism', 'dori_nomi')

@admin.register(Uchrashuv)
class UchrashuvAdmin(admin.ModelAdmin):
    list_display = ('display_bemor', 'display_shifokor', 'sana_va_vaqt', 'holat')
    list_filter = ('holat', 'sana_va_vaqt', 'shifokor')
    search_fields = ('bemor__ism', 'bemor__familiya', 'shifokor__ism', 'shifokor__familiya')

    def display_bemor(self, obj):
        return format_html('<span style="font-weight: bold;">👥 {}</span>', obj.bemor)
    display_bemor.short_description = "Bemor"

    def display_shifokor(self, obj):
        return format_html('<span style="color: #2563eb; font-weight: bold;">👨‍⚕️ {}</span>', obj.shifokor)
    display_shifokor.short_description = "Shifokor"

@admin.register(Amaliyotchi)
class AmaliyotchiAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'display_ustoz', 'kelgan_sana')
    list_filter = ('ustoz_shifokor', 'kelgan_sana')

    def display_ustoz(self, obj):
        if obj.ustoz_shifokor:
            return format_html('<span style="color: #2563eb; font-weight: bold;">👨‍⚕️ {}</span>', obj.ustoz_shifokor)
        return "-"
    display_ustoz.short_description = "Ustoz shifokor"

@admin.register(TibbiyYozuv)
class TibbiyYozuvAdmin(admin.ModelAdmin):
    list_display = ('display_bemor', 'display_shifokor', 'yozuv_sanasi', 'tashxis')
    list_filter = ('yozuv_sanasi', 'shifokor')
    search_fields = ('bemor__ism', 'bemor__familiya', 'tashxis')

    def display_bemor(self, obj):
        return format_html('<span style="font-weight: bold;">👥 {}</span>', obj.bemor)
    display_bemor.short_description = "Bemor"

    def display_shifokor(self, obj):
        return format_html('<span style="color: #2563eb; font-weight: bold;">👨‍⚕️ {}</span>', obj.shifokor)
    display_shifokor.short_description = "Shifokor"
