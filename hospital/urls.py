from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.index, name='index'),
    path('patient/<int:pk>/pdf/', views.generate_patient_pdf, name='patient_pdf'),
    path('doctor/<int:pk>/pdf/', views.generate_doctor_pdf, name='doctor_pdf'),
    path('xonalar/', views.xonalar_boshqaruvi, name='xonalar'),
]

