from django.db import models

# Create your models here.

class Ruta(models.Model):

    TIPOS_RUTA = (
        ('Nacional', 'Nacional'),
        ('Provincial', 'Provincial'),
        ('Municipal', 'Muncipal'),
    )

    nombre = models.CharField(("Nombre Ruta:"), max_length=50)
    tipo = models.CharField(("Tipo Ruta:"), max_length=50, choices=TIPOS_RUTA)
    coordenadas = models.CharField(("Coordenada Ruta:"), max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.tipo}"

    def listar_estaciones(self):
        return Estacion.objects.filter(id_ruta=self)
    
    def agregar_estacion(self):
        pass

    def eliminar_estacion(self):
        pass

    def getNombre(self):
        pass

    def setNombre(self):
        pass

    def getTipo(self):
        pass

    def setTipo(self):
        pass

    def getCoordenadas(self):
        pass

    def setCoordenadas(self):
        pass


class Estacion(models.Model):
    numero_estacion = models.IntegerField(("Numero Estacion:"))
    km_ruta = models.IntegerField(("KM Ruta:"))
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Estacion N°{self.numero_estacion}"
    
    def abrir_casilla(self):
        pass

    def cerrar_casilla(self):
        pass

    def getNumero_estacion(self):
        pass

    def setNumero_estacion(self):
        pass 


class Casilla(models.Model):
    num_casilla = models.IntegerField(("Numero Casilla:"))
    estado = models.BooleanField(("Abierto:"), default=True)
    id_estacion = models.ForeignKey(Estacion,on_delete=models.CASCADE)

    def __str__(self):
        return f"Casilla {self.num_casilla} de Estación N°{self.id_estacion.numero_estacion}"

    def emitir_ticket(self):
        pass

    def registrar_cobro(self):
        pass

    def cambiar_estado(self):
        pass

    def generar_reporte_casilla(self):
        pass

class Usuario(models.Model):
    nombre = models.CharField(("Nombre:"), max_length=50)
    apellido = models.CharField(("Apellido:"), max_length=50)
    direccion = models.CharField(("Direccion:"), max_length=50) 
    email = models.EmailField(("Email:"), max_length=254)
    tipo_documento = models.CharField(("Tipo Documento:"), max_length=50)
    numero_documento = models.CharField(("Numero Documento:"), max_length=50)
    password = models.CharField(("Password:"), max_length=50)
    permisos = models.BooleanField(("Admin:"))

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def iniciar_sesion(self):
        pass

    def cambiar_permisos(self):
        if self.permisos == True:
            self.permisos = False
        else:
            self.permisos = True

    def modificar_datos(self, n_nombre, n_apellido, n_direccion):
        self.nombre = n_nombre
        self.apellido = n_apellido
        self.direccion = n_direccion
        self.save()


class TurnoTrabajo(models.Model):
    fh_inicio = models.DateTimeField(("Fecha y Hora Incio:"), auto_now=False, auto_now_add=False)
    fh_fin = models.DateTimeField(("Fecha y Hora Final:"), auto_now=False, auto_now_add=False)
    sentido_cobro = models.CharField(("Sentido de Cobro:"), max_length=100)
    monto_inicial = models.DecimalField(("Monto Inicial:"),max_digits=5,decimal_places=2)
    enlace_reporte = models.CharField(("Enlace Reporte:"), max_length=50)
    estado = models.BooleanField(("Estado:"), default=True)
    id_casilla = models.ForeignKey(Casilla,on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)

    def __str__(self):
        return f"Turno ID: {self.pk}, Inicio: {self.fh_inicio}, Final: {self.fh_fin}, Operador: {self.id_usuario.nombre} {self.id_usuario.apellido}"

    def iniciar_turno(self):
        pass
    
    def cerrar_turno(self):
        pass

    def duracion_turno(self):
        pass

    def generar_reporte_turno(self):
        pass

    def ingresar_monto_inicial(self):
        pass

class Tarifa(models.Model):
    CATEGORIAS_VEHICULO = (
        ('motocicleta', 'Motocicleta'),
        ('automoviles', 'Automóviles'),
        ('2_ejes_duales', '2 Ejes con Ruedas Duales o Altura Mayor a 2.10m'),
        ('3_4_ejes', '3 o 4 Ejes, Sin Ruedas Duales y Altura Menor a 2.10m'),
        ('5_6_ejes', '5 o 6 Ejes'),
        ('mas_de_6_ejes', 'Más de 6 Ejes'),
    )

    categoria = models.CharField(("Categoria Vehiculo"), max_length=50, choices=CATEGORIAS_VEHICULO)
    monto = models.DecimalField(("Monto:"), max_digits=5,decimal_places=2)
    fecha_modificacion = models.DateField(("Fecha Modificacion:"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.get_categoria_display()} - Monto: {self.monto}"

    def modif_tarifa(self):
        pass

class RegistroCobro(models.Model):
    fh_emision = models.DateTimeField(("Fecha y Hora Emision:"), auto_now=False, auto_now_add=False)
    id_turno = models.ForeignKey(TurnoTrabajo,on_delete=models.CASCADE)
    id_tarifa = models.ForeignKey(Tarifa,on_delete=models.CASCADE)

    def __str__(self):
        return f"Registro de Cobro - Emisión: {self.fh_emision}, Turno: {self.id_turno}, Tarifa: {self.id_tarifa}"

    def generar_informe_caja(self):
        pass