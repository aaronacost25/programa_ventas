from django.db import models

class Prueba(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulos = models.CharField(max_length=200)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.titulo

from django.db import models
from applications.productos.models import Producto


from django.contrib.auth.models import User

class Venta(models.Model):
    MEDIOS_PAGO = [
    ('efectivo', 'Efectivo'),
    ('transferencia', 'Transferencia'),
    ('qr', 'QR'),
    ('debito', 'Débito'),
    ('credito', 'Crédito'),
]
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    medio_pago = models.CharField(max_length=20, choices=MEDIOS_PAGO, default='efectivo')
    cerrada = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha} - {self.medio_pago} - {self.usuario}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"
    
from django.contrib.auth.models import User
    
class CierreCaja(models.Model):

    fecha = models.DateField()

    total_sistema = models.DecimalField(max_digits=12, decimal_places=2)

    efectivo_sistema = models.DecimalField(max_digits=12, decimal_places=2)
    transferencia_sistema = models.DecimalField(max_digits=12, decimal_places=2)

    qr_sistema   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debito_sistema = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credito_sistema = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    monto_real = models.DecimalField(max_digits=12, decimal_places=2)

    diferencia = models.DecimalField(max_digits=12, decimal_places=2)

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    fecha_cierre = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cierre {self.fecha} - Diferencia: {self.diferencia}"

class AperturaCaja(models.Model):

    fecha = models.DateField()

    monto_inicial = models.DecimalField(max_digits=12, decimal_places=2)

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    fecha_apertura = models.DateTimeField(auto_now_add=True)

    abierta = models.BooleanField(default=True)

    class Meta:
        unique_together = ('fecha', 'usuario')

    def __str__(self):
        return f"Apertura {self.fecha} - {self.usuario}"

class Gasto(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.descripcion