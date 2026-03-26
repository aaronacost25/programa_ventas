"""
URL configuration for empleados project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from . import views
from .views import venta , abrir_caja


urlpatterns = [
    path('prueba/',views.PruebaView.as_view(), name='prueba'),
    path('listar-prueba/',views.ListarPrueba.as_view(), name='listar_prueba'),
    path('venta/', venta, name='venta') , 
    path('ticket/<int:venta_id>/', views.ticket, name='ticket'),
    path('reporte-diario/', views.reporte_diario, name='reporte_diario'),
    path('cierre-caja/', views.cierre_caja, name='cierre_caja'),
    path('cierre-caja/cerrar/', views.cierre_caja, name='cerrar_caja'),
    path('abrir-caja/', abrir_caja, name='abrir_caja'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.inicio, name='inicio'),
    path('registrar-gasto/', views.registrar_gasto, name='registrar_gasto'),
    path('reimprimir/<int:venta_id>/', views.reimprimir_venta, name='reimprimir_venta'),
]
