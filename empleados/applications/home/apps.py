from django.apps import AppConfig
from django.views.generic import TemplateView


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.home'


class VentaView(TemplateView):
    template_name = 'home/venta.html'