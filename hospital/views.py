from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Shifokor, Bemor, Kasallik, Uchrashuv, Amaliyotchi, TibbiyYozuv, Retsept
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone

def index(request):
    shifokorlar = Shifokor.objects.all()
    bemorlar = Bemor.objects.order_by('-kelgan_vaqti')[:10]
    context = {
        'shifokorlar_soni': Shifokor.objects.count(),
        'amaliyotchilar_soni': Amaliyotchi.objects.count(),
        'kasal_bemorlar_soni': Bemor.objects.filter(holati='kasal').count(),
        'tuzalgan_bemorlar_soni': Bemor.objects.filter(holati='tuzalgan').count(),
        'bemorlar': bemorlar,
        'shifokorlar': shifokorlar,
    }
    kasallik_qs = Kasallik.objects.annotate(b_count=Count('bemorlar')).order_by('-b_count')[:7]
    context['chart_labels'] = [k.nomi for k in kasallik_qs]
    context['chart_data'] = [k.b_count for k in kasallik_qs]
    return render(request, 'hospital/index.html', context)

def generate_patient_pdf(request, pk):
    bemor = get_object_or_404(Bemor, pk=pk)
    yozuvlar = TibbiyYozuv.objects.filter(bemor=bemor).order_by('-yozuv_sanasi')
    uchrashuvlar = Uchrashuv.objects.filter(bemor=bemor).order_by('-sana_va_vaqt')
    retseptlar = Retsept.objects.filter(bemor=bemor).order_by('-sana')
    template = get_template('hospital/patient_report_pdf.html')
    context = {'bemor': bemor, 'yozuvlar': yozuvlar, 'uchrashuvlar': uchrashuvlar, 'retseptlar': retseptlar, 'bugun': timezone.now()}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_patient_{bemor.ism}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def generate_doctor_pdf(request, pk):
    shifokor = get_object_or_404(Shifokor, pk=pk)
    bemorlar = Bemor.objects.filter(kasalligi__in=shifokor.kasallik_yonalishlari.all()).distinct()
    uchrashuvlar = Uchrashuv.objects.filter(shifokor=shifokor).order_by('-sana_va_vaqt')
    
    template = get_template('hospital/doctor_report_pdf.html')
    context = {
        'shifokor': shifokor,
        'bemorlar': bemorlar,
        'uchrashuvlar': uchrashuvlar,
        'bugun': timezone.now()
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_doctor_{shifokor.familiya}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response
