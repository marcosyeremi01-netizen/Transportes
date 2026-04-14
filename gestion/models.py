from django.db import models

# Bus
class Bus(models.Model):
    placa = models.CharField(max_length=20, unique=True)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.placa

# Representa un autobús con su placa unica y capacidad de pasajeros


# Pasajero
class Pasajero(models.Model):
    nombre = models.CharField(max_length=100)
    dpi = models.CharField(max_length=20, unique=True)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre

# una persona registrada que puede comprar boletos


# Ruta
class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.origen} - {self.destino}"

# Define el recorrido del viaje con origen, destino y costo


# Viaje
class Viaje(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.ruta} - {self.fecha} {self.hora}"

# un viaje programado con un bus, ruta, fecha y hora


# Boleto
class Boleto(models.Model):
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    asiento = models.IntegerField()

    def __str__(self):
        return f"Asiento {self.asiento} - {self.viaje}"

# la compra de un asiento por un pasajero en un viaje específico
