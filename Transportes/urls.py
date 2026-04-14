"""
URL configuration for Transportes project.

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

from django.urls import path
from .views import lista_viajes, registrar_pasajero, comprar_boleto, crear_bus, crear_ruta, crear_viaje, editar_bus, editar_ruta, editar_viaje
from .views import descargar_boleto, registro, iniciar_sesion, cerrar_sesion

urlpatterns = [
    path('', lista_viajes, name='viajes'),
    path('pasajero/', registrar_pasajero, name='pasajero'),
    path('boleto/', comprar_boleto, name='boleto'),
    path('bus/', crear_bus, name='bus'),
    path('ruta/', crear_ruta, name='ruta'),
    path('viaje/', crear_viaje, name='viaje'),
    path('bus/editar/<int:id>/', editar_bus, name='editar_bus'),
    path('ruta/editar/<int:id>/', editar_ruta, name='editar_ruta'),
    path('viaje/editar/<int:id>/', editar_viaje, name='editar_viaje'),
    path('descargar-boleto/', descargar_boleto, name='descargar_boleto'),
    path('registro/', registro, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
]

