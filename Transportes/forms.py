from django import forms
from gestion.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = '__all__'


class BoletoForm(forms.ModelForm):
    class Meta:
        model = Boleto
        fields = '__all__'
        
from django import forms
from gestion.models import Bus, Ruta, Viaje

# Bus
class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'

# Ruta
class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = '__all__'


# Viaje
class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'
        
#LOGIN
class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']