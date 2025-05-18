from django.apps import AppConfig

class UstpCommerceApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ustp_commerce_api'

    def ready(self):
        import ustp_commerce_api.signals
