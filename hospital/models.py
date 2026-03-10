from django.db import models
from django.utils import timezone

class Kasallik(models.Model):
    nomi = models.CharField(max_length=150, verbose_name="Kasallik nomi")
    tavsifi = models.TextField(verbose_name="Tavsifi", null=True, blank=True)
    rasm = models.ImageField(upload_to='kasalliklar/', null=True, blank=True, verbose_name="Kasallik rasmi")

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = "Kasallik turi"
        verbose_name_plural = "Kasallik turlari"

class Shifokor(models.Model):
    ism = models.CharField(max_length=50, verbose_name="Ism")
    familiya = models.CharField(max_length=50, verbose_name="Familiya")
    kasallik_yonalishlari = models.ManyToManyField(Kasallik, verbose_name="Davolaydigan kasalliklari")
    ish_tajribasi_yillar = models.PositiveIntegerField(verbose_name="Ish tajribasi (yil)")
    telefon_raqam = models.CharField(max_length=15, verbose_name="Telefon raqami", null=True, blank=True)
    manzil = models.TextField(verbose_name="Yashash manzili", null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.ism} {self.familiya}"

    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"

class Amaliyotchi(models.Model):
    ism = models.CharField(max_length=50, verbose_name="Ism")
    familiya = models.CharField(max_length=50, verbose_name="Familiya")
    telefon_raqam = models.CharField(max_length=15, verbose_name="Telefon raqami")
    manzil = models.TextField(verbose_name="Yashash manzili")
    ustoz_shifokor = models.ForeignKey(Shifokor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ustoz shifokor")
    kelgan_sana = models.DateField(auto_now_add=True, verbose_name="Amaliyot boshlangan sana")

    def __str__(self):
        return f"Amaliyotchi: {self.ism} {self.familiya}"

    class Meta:
        verbose_name = "Amaliyotchi"
        verbose_name_plural = "Amaliyotchilar"

class Bemor(models.Model):
    HOLAT_CHOICES = (
        ('kasal', 'Davolanmoqda (Kasal)'),
        ('tuzalgan', 'Tuzalib ketgan'),
    )

    ism = models.CharField(max_length=50, verbose_name="Ism")
    familiya = models.CharField(max_length=50, verbose_name="Familiya")
    telefon_raqam = models.CharField(max_length=15, verbose_name="Telefon raqami")
    tugilgan_sana = models.DateField(verbose_name="Tug'ilgan sana", null=True, blank=True)
    manzil = models.TextField(verbose_name="Yashash manzili", null=True, blank=True)
    
    kasalligi = models.ForeignKey(Kasallik, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kasalligi")
    holati = models.CharField(max_length=20, choices=HOLAT_CHOICES, default='kasal', verbose_name="Holati")
    kelgan_vaqti = models.DateTimeField(default=timezone.now, verbose_name="Kelgan vaqti")
    tuzalgan_vaqti = models.DateTimeField(null=True, blank=True, verbose_name="Tuzalgan vaqti")

    def __str__(self):
        return f"{self.ism} {self.familiya}"

    class Meta:
        verbose_name = "Bemor"
        verbose_name_plural = "Bemorlar"

class Uchrashuv(models.Model):
    STATUS_CHOICES = (
        ('kutilmoqda', 'Kutilmoqda'),
        ('yakunlandi', 'Yakunlandi'),
        ('bekor_qilindi', 'Bekor qilindi'),
    )

    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE, verbose_name="Bemor")
    shifokor = models.ForeignKey(Shifokor, on_delete=models.CASCADE, verbose_name="Shifokor")
    sana_va_vaqt = models.DateTimeField(verbose_name="Uchrashuv sanasi va vaqti")
    holat = models.CharField(max_length=20, choices=STATUS_CHOICES, default='kutilmoqda', verbose_name="Holat")

    def __str__(self):
        return f"{self.bemor} - {self.shifokor} ({self.sana_va_vaqt.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Uchrashuv"
        verbose_name_plural = "Uchrashuvlar"

class TibbiyYozuv(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE, verbose_name="Bemor")
    shifokor = models.ForeignKey(Shifokor, on_delete=models.SET_NULL, null=True, verbose_name="Shifokor")
    tashxis = models.TextField(verbose_name="Tashxis")
    tavsiyalar = models.TextField(verbose_name="Davolash tavsiyalari", null=True, blank=True)
    yozuv_sanasi = models.DateTimeField(auto_now_add=True, verbose_name="Yozuv sanasi")
    uchrashuv = models.OneToOneField(Uchrashuv, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bog'liq uchrashuv")

    def __str__(self):
        return f"{self.bemor} uchun tashxis ({self.yozuv_sanasi.strftime('%Y-%m-%d')})"

    class Meta:
        verbose_name = "Tibbiy yozuv"
        verbose_name_plural = "Tibbiy yozuvlar"
