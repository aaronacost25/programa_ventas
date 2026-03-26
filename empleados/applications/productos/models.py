from django.db import models

# Create your models here.
from django.db import models

class Producto(models.Model):

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.codigo}"