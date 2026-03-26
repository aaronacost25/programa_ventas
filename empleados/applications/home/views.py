from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import ExtractHour
from decimal import Decimal
from datetime import datetime
from applications.productos.models import Producto
from .models import Gasto, Venta, DetalleVenta, AperturaCaja, CierreCaja, Prueba
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import base64


# ------------------------------
# PRUEBA
# ------------------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from .models import AperturaCaja

@login_required
def inicio(request):

    fecha = timezone.localdate()

    apertura = AperturaCaja.objects.filter(
        fecha=fecha,
        usuario=request.user,
        abierta=True
    ).first()

    if apertura:
        return redirect('venta')  # ya abrió caja → va a ventas
    else:
        return redirect('abrir_caja')  # no abrió → abrir caja
class PruebaView(TemplateView):
    template_name = "home/prueba.html"


class ListarPrueba(ListView):
    model = Prueba
    template_name = "home/listar_prueba.html"
    context_object_name = "lista"


# ------------------------------
# VENTAS
# ------------------------------

@login_required
def venta(request):

    if 'carrito' not in request.session:
        request.session['carrito'] = []

    carrito = request.session['carrito']
    error = None
    total = Decimal('0.00')

    # ACTUALIZAR CANTIDAD
    if request.method == 'POST' and 'actualizar' in request.POST:

        codigo = request.POST.get('actualizar')
        nueva_cantidad = request.POST.get('nueva_cantidad')

        if not nueva_cantidad:
            return redirect('venta')

        nueva_cantidad = float(nueva_cantidad)

        for item in carrito:
            if item['codigo'] == codigo:

                producto = Producto.objects.get(codigo=codigo)

                if producto.stock >= nueva_cantidad:
                    item['cantidad'] = nueva_cantidad
                    item['subtotal'] = float(producto.precio) * nueva_cantidad

        request.session['carrito'] = carrito
        return redirect('venta')

    # ELIMINAR PRODUCTO
    if request.method == 'POST' and 'eliminar' in request.POST:

        codigo = request.POST.get('eliminar')
        carrito = [item for item in carrito if item['codigo'] != codigo]

        request.session['carrito'] = carrito
        return redirect('venta')

    # FINALIZAR VENTA
    if request.method == 'POST' and 'finalizar' in request.POST:

        medio_pago = request.POST.get('medio_pago', 'efectivo')

        if not carrito:
            error = "No hay productos en la venta"

        else:

            total_venta = Decimal('0')

            for item in carrito:
                total_venta += Decimal(str(item['subtotal']))

            nueva_venta = Venta.objects.create(
                total=total_venta,
                medio_pago=medio_pago,
                usuario=request.user
            )

            for item in carrito:

                producto = Producto.objects.get(codigo=item['codigo'])
                cantidad = Decimal(str(item['cantidad']))

                if producto.stock >= cantidad:

                    producto.stock -= cantidad
                    producto.save()

                    DetalleVenta.objects.create(
                        venta=nueva_venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio=producto.precio,
                        subtotal=producto.precio * cantidad
                    )

                else:

                    error = f"Stock insuficiente para {producto.nombre}"
                    nueva_venta.delete()
                    break

            if not error:
                request.session['carrito'] = []
                return redirect('ticket', venta_id=nueva_venta.id)

    # AGREGAR PRODUCTO
    elif request.method == 'POST':

        codigo = request.POST.get('codigo')
        cantidad = request.POST.get('cantidad')

        try:

            producto = Producto.objects.get(codigo=codigo)
            cantidad = Decimal(cantidad)

            if producto.stock < cantidad:
                error = "Stock insuficiente"

            else:

                subtotal = producto.precio * cantidad

                carrito.append({
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'precio': float(producto.precio),
                    'cantidad': float(cantidad),
                    'subtotal': float(subtotal)
                })

                request.session['carrito'] = carrito

        except:
            error = "Producto no encontrado"

    for item in carrito:
        total += Decimal(str(item['subtotal']))
    apertura = AperturaCaja.objects.filter(
    fecha=timezone.localdate(),
    usuario=request.user,
    abierta=True
    ).first()

    if not apertura:
        return redirect('abrir_caja')

    return render(request, 'home/venta.html', {
        'carrito': carrito,
        'total': total,
        'error': error
    })


# ------------------------------
# TICKET
# ------------------------------

@login_required
def ticket(request, venta_id):

    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    return render(request, 'home/ticket.html', {
        'venta': venta,
        'detalles': detalles
    })


# ------------------------------
# APERTURA CAJA
# ------------------------------

@login_required
def abrir_caja(request):

    fecha = timezone.localdate()

    if request.method == "POST":

        monto_inicial = Decimal(request.POST.get('monto_inicial'))

        apertura, creada = AperturaCaja.objects.get_or_create(
            fecha=fecha,
            usuario=request.user,
            defaults={
                'monto_inicial': monto_inicial
            }
        )

        return redirect('cierre_caja')

    return render(request, 'home/abrir_caja.html')

# ------------------------------
# CIERRE CAJA
# ------------------------------from decimal import Decimal
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum

def cierre_caja(request):

    fecha = timezone.localdate()

    ventas = Venta.objects.filter(
        fecha__date=fecha,
        usuario=request.user
    )
    gastos = Gasto.objects.filter(
    fecha__date=fecha,
    usuario=request.user
)

    total_general = ventas.aggregate(total=Sum('total'))['total'] or Decimal('0')
    total_efectivo = ventas.filter(medio_pago='efectivo').aggregate(total=Sum('total'))['total'] or Decimal('0')
    total_transferencia = ventas.filter(medio_pago='transferencia').aggregate(total=Sum('total'))['total'] or Decimal('0')
    total_qr = ventas.filter(medio_pago='qr').aggregate(total=Sum('total'))['total'] or Decimal('0')
    total_debito = ventas.filter(medio_pago='debito').aggregate(total=Sum('total'))['total'] or Decimal('0')
    total_credito = ventas.filter(medio_pago='credito').aggregate(total=Sum('total'))['total'] or Decimal('0')

    total_gastos = Gasto.objects.filter(
        fecha__date=fecha,
        usuario=request.user
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    apertura = AperturaCaja.objects.filter(
        fecha=fecha,
        usuario=request.user,
        abierta=True
    ).first()

    cierre = CierreCaja.objects.filter(
        fecha=fecha,
        usuario=request.user
    ).first()

    color_diferencia = "green"

    if cierre:
        if cierre.diferencia < 0:
            color_diferencia = "red"
        elif cierre.diferencia > 0:
            color_diferencia = "orange"

    if request.method == "POST":

        if not apertura:
            return redirect('abrir_caja')

        if cierre:
            return redirect('cierre_caja')

        monto_real = Decimal(request.POST.get('monto_real') or 0)
        monto_inicial = apertura.monto_inicial

        # efectivo real esperado descontando gastos
        total_esperado = monto_inicial + total_efectivo - total_gastos

        diferencia = monto_real - total_esperado

        cierre = CierreCaja.objects.create(
            fecha=fecha,
            total_sistema=total_general,
            efectivo_sistema=total_esperado,
            transferencia_sistema=total_transferencia,
            qr_sistema=total_qr,
            debito_sistema=total_debito,
            credito_sistema=total_credito,
            monto_real=monto_real,
            diferencia=diferencia,
            usuario=request.user
        )

        apertura.abierta = False
        apertura.save()

        if diferencia < 0:
            color_diferencia = "red"
        elif diferencia > 0:
            color_diferencia = "orange"
        else:
            color_diferencia = "green"

    return render(request, 'home/cierre_caja.html', {
        'fecha': fecha,
        'ventas': ventas,
        'total_general': total_general,
        'total_efectivo': total_efectivo,
        'total_transferencia': total_transferencia,
        'total_qr': total_qr,
        'total_debito': total_debito,
        'total_credito': total_credito,
        'total_gastos': total_gastos,
        'apertura': apertura,
        'cierre': cierre,
        'color_diferencia': color_diferencia , 
        'gastos': gastos,
    })

@login_required
def reporte_diario(request):

    hoy = timezone.localdate()

    ventas = Venta.objects.filter(
        fecha__date=hoy
    ).prefetch_related('detalleventa_set__producto')

    total = ventas.aggregate(total=Sum('total'))['total'] or 0

    return render(request, 'home/reporte.html', {
        'ventas': ventas,
        'total_hoy': total,
        'cantidad_ventas': ventas.count(),
        'hoy': hoy
    })


# ------------------------------
# RESUMEN POR EMPLEADO
# ------------------------------

@login_required
def resumen_dia(request):

    fecha = timezone.localdate()
    usuarios = User.objects.all()

    resumen = []
    total_efectivo = 0
    total_transferencia = 0

    for usuario in usuarios:

        ventas = Venta.objects.filter(
            fecha__date=fecha,
            usuario=usuario
        )

        efectivo = ventas.filter(medio_pago='efectivo').aggregate(total=Sum('total'))['total'] or 0
        transferencia = ventas.filter(medio_pago='transferencia').aggregate(total=Sum('total'))['total'] or 0

        resumen.append({
            'usuario': usuario,
            'efectivo': efectivo,
            'transferencia': transferencia
        })

        total_efectivo += efectivo
        total_transferencia += transferencia

    return render(request, 'home/resumen_dia.html', {
        'resumen_empleados': resumen,
        'total_efectivo_dia': total_efectivo,
        'total_transferencia_dia': total_transferencia,
        'total_general': total_efectivo + total_transferencia
    })


# ------------------------------
# DASHBOARD
# ------------------------------

@login_required
def dashboard(request):

    fecha = timezone.localdate()

    ventas = Venta.objects.filter(fecha__date=fecha)

    ventas_por_empleado = Venta.objects.filter(
        fecha__date=fecha
    ).values(
        'usuario__username'
    ).annotate(
        total=Sum('total'),
        cantidad=Count('id')
    )

    productos_vendidos = DetalleVenta.objects.filter(
        venta__fecha__date=fecha
    ).values(
        'producto__nombre'
    ).annotate(
        total=Sum('cantidad')
    ).order_by('-total')[:5]

    empleados = []
    totales = []

    for venta in ventas_por_empleado:
        empleados.append(venta['usuario__username'])
        totales.append(float(venta['total']))

    cajas_abiertas = AperturaCaja.objects.filter(
        fecha=fecha,
        abierta=True
    )

    total_gastos = Gasto.objects.filter(
        fecha__date=fecha
    ).aggregate(total=Sum('monto'))['total'] or 0

    ventas_por_hora = Venta.objects.filter(
    fecha__date=fecha
    ).annotate(
        hora=ExtractHour('fecha')
    ).values(
        'hora'
    ).annotate(
        total=Sum('total')
    ).order_by('hora')


    horas = []
    totales_hora = []

    for item in ventas_por_hora:
        horas.append(f"{item['hora']}:00")
        totales_hora.append(float(item['total']))

    return render(request, 'home/dashboard.html', {
        'fecha': fecha,
        'total_ventas': ventas.aggregate(Sum('total'))['total__sum'] or 0,
        'cantidad_ventas': ventas.count(),
        'total_efectivo': ventas.filter(medio_pago='efectivo').aggregate(Sum('total'))['total__sum'] or 0,
        'total_transferencia': ventas.filter(medio_pago='transferencia').aggregate(Sum('total'))['total__sum'] or 0,
        'total_qr': ventas.filter(medio_pago='qr').aggregate(Sum('total'))['total__sum'] or 0,
        'total_gastos': total_gastos,
        'productos_vendidos': productos_vendidos,
        'ventas_por_empleado': ventas_por_empleado,
        'empleados': empleados,
        'totales': totales,
        'cajas_abiertas': cajas_abiertas,
        'horas': horas,
        'totales_hora': totales_hora,
    })
@login_required
def registrar_gasto(request):

    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        monto = Decimal(request.POST.get('monto'))

        Gasto.objects.create(
            descripcion=descripcion,
            monto=monto,
            usuario=request.user
        )

        return redirect('cierre_caja')

    return render(request, 'home/registrar_gasto.html')



from django.shortcuts import render, get_object_or_404
from .models import Venta

def reimprimir_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    return render(request, 'home/ticket.html', {
        'venta': venta
    })