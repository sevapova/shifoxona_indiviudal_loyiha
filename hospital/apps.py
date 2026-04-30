from django.apps import AppConfig

class HospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital'
    verbose_name = '🏥 Shifoxona bo\'limi'

    def ready(self):
        import hospital.signals
