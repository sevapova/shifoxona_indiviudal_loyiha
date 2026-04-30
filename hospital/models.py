from django.db import models
from django.utils import timezone

class Kasallik(models.Model):
    nomi = models.CharField(max_length=200, verbose_name="Kasallik nomi")
    tavsifi = models.TextField(verbose_name="Tavsifi", null=True, blank=True)
    rasm = models.ImageField(upload_to='diseases/', null=True, blank=True, verbose_name="Rasm")
    def __str__(self): return self.nomi
    class Meta:
        verbose_name = "Kasallik"
        verbose_name_plural = "Kasalliklar"

class Shifokor(models.Model):
    ism = models.CharField(max_length=100, verbose_name="Ismi")
    familiya = models.CharField(max_length=100, verbose_name="Familiyasi")
    mutaxassislik = models.CharField(max_length=200, verbose_name="Mutaxassisligi", null=True, blank=True)
    kasallik_yonalishlari = models.ManyToManyField(Kasallik, verbose_name="Davolaydigan kasalliklari", blank=True)
    ish_tajribasi_yillar = models.PositiveIntegerField(default=0, verbose_name="Ish tajribasi (yil)")
    telefon_raqam = models.CharField(max_length=20, verbose_name="Telefon raqami", null=True, blank=True)
    manzil = models.TextField(verbose_name="Manzili", null=True, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name="Telegram ID")
    parol = models.CharField(max_length=50, null=True, blank=True, verbose_name="Parol")
    def __str__(self): return f"Dr. {self.ism} {self.familiya}"
    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"

class Bemor(models.Model):
    HOLAT_CHOICES = [('kasal', 'Davolanmoqda'), ('tuzalgan', 'Tuzalgan')]
    ism = models.CharField(max_length=100, verbose_name="Ismi")
    familiya = models.CharField(max_length=100, verbose_name="Familiyasi")
    telefon_raqam = models.CharField(max_length=20, verbose_name="Telefon raqami", null=True, blank=True)
    tugilgan_sana = models.DateField(verbose_name="Tug'ilgan sana", null=True, blank=True)
    manzil = models.TextField(verbose_name="Yashash manzili", null=True, blank=True)
    kasalligi = models.ForeignKey(Kasallik, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kasalligi", related_name='bemorlar')
    holati = models.CharField(max_length=20, choices=HOLAT_CHOICES, default='kasal', verbose_name="Holati")
    kelgan_vaqti = models.DateTimeField(default=timezone.now, verbose_name="Kelgan vaqti")
    tuzalgan_vaqti = models.DateTimeField(null=True, blank=True, verbose_name="Tuzalgan vaqti")
    telegram_id = models.BigIntegerField(null=True, blank=True, verbose_name="Telegram ID")
    parol = models.CharField(max_length=50, null=True, blank=True, verbose_name="Parol")
    def __str__(self): return f"{self.ism} {self.familiya}"
    class Meta:
        verbose_name = "Bemor"
        verbose_name_plural = "Bemorlar"

class Retsept(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE, verbose_name="Bemor")
    shifokor = models.ForeignKey(Shifokor, on_delete=models.CASCADE, verbose_name="Shifokor")
    dori_nomi = models.CharField(max_length=255, verbose_name="Dori nomi")
    dozalash = models.CharField(max_length=100, verbose_name="Dozalash (masalan: 1 kunda 2 mahal)")
    muddati = models.CharField(max_length=100, verbose_name="Muddati")
    izoh = models.TextField(null=True, blank=True, verbose_name="Qo'shimcha izoh")
    sana = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Retsept"
        verbose_name_plural = "Retseptlar"

class Uchrashuv(models.Model):
    HOLAT_CHOICES = [('kutilmoqda', 'Kutilmoqda'), ('yakunlandi', 'Yakunlandi'), ('bekor_qilindi', 'Bekor qilindi')]
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE, verbose_name="Bemor")
    shifokor = models.ForeignKey(Shifokor, on_delete=models.CASCADE, verbose_name="Shifokor")
    sana_va_vaqt = models.DateTimeField(verbose_name="Uchrashuv vaqti")
    holat = models.CharField(max_length=20, choices=HOLAT_CHOICES, default='kutilmoqda', verbose_name="Holati")
    def __str__(self): return f"{self.bemor} - Dr. {self.shifokor} ({self.sana_va_vaqt})"
    class Meta:
        verbose_name = "Uchrashuv"
        verbose_name_plural = "Uchrashuvlar"

class Amaliyotchi(models.Model):
    ism = models.CharField(max_length=100, verbose_name="Ismi")
    familiya = models.CharField(max_length=100, verbose_name="Familiyasi")
    telefon_raqam = models.CharField(max_length=20, verbose_name="Telefon raqami", null=True, blank=True)
    manzil = models.TextField(verbose_name="Manzili", null=True, blank=True)
    ustoz_shifokor = models.ForeignKey(Shifokor, on_delete=models.SET_NULL, null=True, verbose_name="Ustoz shifokor")
    kelgan_sana = models.DateField(default=timezone.now, verbose_name="Kelgan sanasi")
    def __str__(self): return f"Intern {self.ism} {self.familiya}"
    class Meta:
        verbose_name = "Amaliyotchi"
        verbose_name_plural = "Amaliyotchilar"

class TibbiyYozuv(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE, verbose_name="Bemor")
    shifokor = models.ForeignKey(Shifokor, on_delete=models.SET_NULL, null=True, verbose_name="Shifokor")
    yozuv_sanasi = models.DateTimeField(default=timezone.now, verbose_name="Sana")
    tashxis = models.TextField(verbose_name="Tashxis")
    tavsiyalar = models.TextField(verbose_name="Tavsiyalar", null=True, blank=True)
    def __str__(self): return f"Record: {self.bemor} ({self.yozuv_sanasi})"
    class Meta:
        verbose_name = "Tibbiy yozuv"
        verbose_name_plural = "Tibbiy yozuvlar"
