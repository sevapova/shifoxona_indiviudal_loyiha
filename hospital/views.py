from django.shortcuts import render
from .models import Shifokor, Bemor, Uchrashuv, Kasallik, Amaliyotchi

def index(request):
    shifokorlar_soni = Shifokor.objects.count()
    bemorlar_soni = Bemor.objects.count()
    kasal_bemorlar_soni = Bemor.objects.filter(holati='kasal').count()
    tuzalgan_bemorlar_soni = Bemor.objects.filter(holati='tuzalgan').count()
    uchrashuvlar_soni = Uchrashuv.objects.count()
    amaliyotchilar_soni = Amaliyotchi.objects.count()
    kasalliklar_soni = Kasallik.objects.count()

    shifokorlar = Shifokor.objects.all().prefetch_related('kasallik_yonalishlari')[:5]
    bemorlar = Bemor.objects.all().order_by('-kelgan_vaqti')[:5]
    kasalliklar = Kasallik.objects.all()[:5]

    context = {
        'shifokorlar_soni': shifokorlar_soni,
        'bemorlar_soni': bemorlar_soni,
        'kasal_bemorlar_soni': kasal_bemorlar_soni,
        'tuzalgan_bemorlar_soni': tuzalgan_bemorlar_soni,
        'uchrashuvlar_soni': uchrashuvlar_soni,
        'amaliyotchilar_soni': amaliyotchilar_soni,
        'kasalliklar_soni': kasalliklar_soni,
        
        'shifokorlar': shifokorlar,
        'bemorlar': bemorlar,
        'kasalliklar': kasalliklar,
    }
    return render(request, 'hospital/index.html', context)
