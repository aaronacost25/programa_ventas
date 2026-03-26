from django.contrib import admin

from .models import Prueba
admin.site.register(Prueba)
from django.contrib import admin
from .models import Venta, DetalleVenta

admin.site.register(Venta)
admin.site.register(DetalleVenta)