from django.db import models

# Create your models here.

class Ruta(models.Model):
    nombre = models.CharField(("Nombre Ruta:"), max_length=50)
    tipo = models.CharField(("Tipo Ruta:"), max_length=50)
    coordenadas = models.CharField(("Coordenada Ruta:"), max_length=50)


class Estacion(models.Model):
    numero_estacion = models.IntegerField(("Numero Estacion:"))
    km_ruta = models.IntegerField(("KM Ruta:"))
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)


class Casilla(models.Model):
    num_casilla = models.IntegerField(("Numero Casilla:"))
    id_estacion = models.ForeignKey(Estacion,on_delete=models.CASCADE)


class Usuario(models.Model):
    nombre = models.CharField(("Nombre:"), max_length=50)
    apellido = models.CharField(("Apellido:"), max_length=50)
    direccion = models.CharField(("Direccion:"), max_length=50) 
    email = models.EmailField(("Email:"), max_length=254)
    tipo_documento = models.CharField(("Tipo Documento:"), max_length=50)
    numero_documento = models.CharField(("Numero Documento:"), max_length=50)
    password = models.CharField(("Password:"), max_length=50)
    permisos = models.BooleanField(("Permiso:"))


class TurnoTrabajo(models.Model):
    fh_inicio = models.DateTimeField(("Fecha y Hora Incio:"), auto_now=False, auto_now_add=False)
    fh_fin = models.DateTimeField(("Fecha y Hora Final:"), auto_now=False, auto_now_add=False)
    sentido_cobro = models.CharField(("Sentido de Cobro:"), max_length=100)
    monto_inicial = models.DecimalField(("Monto Inicial:"),max_digits=5,decimal_places=2)
    enlace_reporte = models.CharField(("Enlace Reporte:"), max_length=50)
    id_casilla = models.ForeignKey(Casilla,on_delete=models.CASCADE)
    id_operador = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    estado = models.BooleanField(("Estado:"))


class Tarifa(models.Model):
    categoria = models.CharField(("Categoria Vehiculo"), max_length=50)
    monto = models.DecimalField(("Monto:"), max_digits=5,decimal_places=2)
    fecha_modificacion = models.DateField(("Fecha Modificacion:"), auto_now=False, auto_now_add=False)


class RegistroCobro(models.Model):
    fh_emision = models.DateTimeField(("Fecha y Hora Emision:"), auto_now=False, auto_now_add=False)
    id_turno = models.ForeignKey(TurnoTrabajo,on_delete=models.CASCADE)
    id_tarifa = models.ForeignKey(Tarifa,on_delete=models.CASCADE)