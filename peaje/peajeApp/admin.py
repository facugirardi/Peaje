from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ruta, RutaBuscar)
admin.site.register(Estacion)
admin.site.register(Casilla)
admin.site.register(Usuario)
admin.site.register(TurnoTrabajo)
admin.site.register(Tarifa)
admin.site.register(RegistroCobro)