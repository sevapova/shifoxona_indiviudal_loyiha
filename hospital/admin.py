import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Kasallik, Shifokor, Bemor, Uchrashuv, Amaliyotchi, TibbiyYozuv, Retsept

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
    list_display = ('nomi', 'tavsifi')
    search_fields = ('nomi',)

@admin.register(Shifokor)
class ShifokorAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'mutaxassislik', 'ish_tajribasi_yillar', 'telefon_raqam', 'download_report')
    list_filter = ('kasallik_yonalishlari',)
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    actions = [export_shifokorlar_csv]

    def download_report(self, obj):
        url = reverse('hospital:doctor_pdf', args=[obj.pk])
        return format_html('<a class="button" href="{}" style="background:#f06292; color:white; padding:5px 10px; border-radius:5px; text-decoration:none;">📄 Hisobot</a>', url)
    download_report.short_description = 'PDF Hisobot'

@admin.register(Bemor)
class BemorAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'telefon_raqam', 'kasalligi', 'holati', 'kelgan_vaqti', 'download_report')
    list_filter = ('holati', 'kasalligi', 'kelgan_vaqti')
    search_fields = ('ism', 'familiya', 'telefon_raqam')
    date_hierarchy = 'kelgan_vaqti'
    actions = [export_bemorlar_csv]

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
    list_display = ('bemor', 'shifokor', 'sana_va_vaqt', 'holat')
    list_filter = ('holat', 'sana_va_vaqt', 'shifokor')
    search_fields = ('bemor__ism', 'bemor__familiya', 'shifokor__ism', 'shifokor__familiya')

@admin.register(Amaliyotchi)
class AmaliyotchiAdmin(admin.ModelAdmin):
    list_display = ('ism', 'familiya', 'ustoz_shifokor', 'kelgan_sana')
    list_filter = ('ustoz_shifokor', 'kelgan_sana')

@admin.register(TibbiyYozuv)
class TibbiyYozuvAdmin(admin.ModelAdmin):
    list_display = ('bemor', 'shifokor', 'yozuv_sanasi', 'tashxis')
    list_filter = ('yozuv_sanasi', 'shifokor')
    search_fields = ('bemor__ism', 'bemor__familiya', 'tashxis')
