from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Viaje, Boleto, Pasajero, Ruta, Bus
from .forms import PasajeroForm, BoletoForm, BusForm, RutaForm, ViajeForm
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required


# Lista de viajes
@login_required
def lista_viajes(request):
    viajes = Viaje.objects.all()
    datos = []

    for v in viajes:
        ocupados = Boleto.objects.filter(viaje=v).count()
        capacidad = v.bus.capacidad
        disponibles = capacidad - ocupados

        datos.append({
            'viaje': v,
            'ocupados': ocupados,
            'disponibles': disponibles
        })

    return render(request, 'lista.html', {'datos': datos})
# Registrar pasajero
def registrar_pasajero(request):
    form = PasajeroForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'pasajero_form.html', {'form': form})


# Comprar boleto 
def comprar_boleto(request):
    form = BoletoForm(request.POST or None)

    if form.is_valid():
        viaje = form.cleaned_data['viaje']
        asiento = form.cleaned_data['asiento']

        # VALIDAR RANGO DE ASIENTO (NUEVO)
        if asiento < 1 or asiento > viaje.bus.capacidad:
            request.session.pop('boleto_id', None)
            messages.error(request, "El número de asiento no existe en este bus")
            return redirect('boleto')

        # asiento repetido
        if Boleto.objects.filter(viaje=viaje, asiento=asiento).exists():
            request.session.pop('boleto_id', None)
            messages.error(request, "Ese asiento ya está ocupado")
            return redirect('boleto')

        # capacidad del bus
        capacidad = viaje.bus.capacidad
        vendidos = Boleto.objects.filter(viaje=viaje).count()

        if vendidos >= capacidad:
            request.session.pop('boleto_id', None)
            messages.error(request, "No hay más asientos disponibles")
            return redirect('boleto')

        # compra exitosa
        boleto = form.save()

        codigo = f"BT-{datetime.now().year}-{str(boleto.id).zfill(4)}"

        messages.success(
            request,
            f"Boleto {codigo} | Asiento {boleto.asiento}"
        )

        # guardar para descarga
        request.session['boleto_id'] = boleto.id

        return redirect('boleto')

    # INFO DE ASIENTOS
    viajes = Viaje.objects.all()
    info_viajes = []

    for v in viajes:
        ocupados = Boleto.objects.filter(viaje=v).values_list('asiento', flat=True)
        capacidad = v.bus.capacidad

        disponibles = [i for i in range(1, capacidad + 1) if i not in ocupados]

        info_viajes.append({
            'viaje': v,
            'ocupados': list(ocupados),
            'disponibles': disponibles
        })

    return render(request, 'boleto_form.html', {
        'form': form,
        'info_viajes': info_viajes
    })
    
#DESCARGAR BOLETO

def descargar_boleto(request):
    boleto_id = request.session.get('boleto_id')

    if not boleto_id:
        return HttpResponse("No hay boleto disponible")

    boleto = Boleto.objects.get(id=boleto_id)

    contenido = f"""
    ====== BOLETO ======
    Pasajero: {boleto.pasajero}
    Viaje: {boleto.viaje}
    Asiento: {boleto.asiento}
    ====================
    """

    response = HttpResponse(contenido, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="boleto.txt"'

    # BORRAR DESPUÉS DE DESCARGAR
    request.session.pop('boleto_id', None)

    return response

# Crear Bus
def crear_bus(request):
    form = BusForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'bus_form.html', {'form': form})


# Crear Ruta
def crear_ruta(request):
    form = RutaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'ruta_form.html', {'form': form})


# Crear Viaje
def crear_viaje(request):
    form = ViajeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'viaje_form.html', {'form': form})

# Info del viaje 
def lista_viajes(request):
    viajes = Viaje.objects.all()

    datos = []

    for viaje in viajes:
        capacidad = viaje.bus.capacidad
        ocupados = Boleto.objects.filter(viaje=viaje).count()
        disponibles = capacidad - ocupados

        datos.append({
            'viaje': viaje,
            'ocupados': ocupados,
            'disponibles': disponibles
        })

    return render(request, 'lista.html', {'datos': datos})

# Editar Bus
def editar_bus(request, id):
    bus = get_object_or_404(Bus, id=id)
    form = BusForm(request.POST or None, instance=bus)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'bus_form.html', {'form': form})


# Editar Ruta
def editar_ruta(request, id):
    ruta = get_object_or_404(Ruta, id=id)
    form = RutaForm(request.POST or None, instance=ruta)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'ruta_form.html', {'form': form})


# Editar Viaje
def editar_viaje(request, id):
    viaje = get_object_or_404(Viaje, id=id)
    form = ViajeForm(request.POST or None, instance=viaje)
    if form.is_valid():
        form.save()
        return redirect('viajes')
    return render(request, 'viaje_form.html', {'form': form})


# REGISTRO
def registro(request):
    form = RegistroForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('viajes')

    return render(request, 'registro.html', {'form': form})


# LOGIN
def iniciar_sesion(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('viajes')

    return render(request, 'login.html', {'form': form})


# LOGOUT
def cerrar_sesion(request):
    logout(request)
    return redirect('login')

