from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import *
from django.utils import timezone
import datetime
from .models import Usuario
from django.contrib.auth import *
from django.contrib.auth.hashers import make_password
from django.db.utils import *
from django.views.decorators.csrf import csrf_exempt
import pytz
import qrcode
from qrcode.image.pure import PymagingImage
import os
from django.conf import settings


def navbar(request):
    return render(request, 'navbar.html')


def base(request):
    return render(request, 'base.html')


def ticket_view(request):
    argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    hora_actual = datetime.datetime.now(argentina_timezone)
    fecha = datetime.datetime.now(argentina_timezone).date()

    minutos = hora_actual.minute
    if len(str(minutos)) == 1:
        minutos = f'0{minutos}'

    hora = f'{hora_actual.hour}:{minutos}'

    usuario = request.user
    turno = TurnoTrabajo.objects.filter(usuario=usuario).first()

    if turno:
        return render(request, 'ticket.html',  {'fecha': fecha, 'hora': hora, 'turno': turno})
    else:
        return render(request, 'ticket.html',  {'fecha': fecha, 'hora': hora})


class GestionTurnoView(View):
    def get(self, request):

        usuario = request.user
        turno = TurnoTrabajo.objects.filter(usuario=usuario).first()

        if turno:
            estado_turno = turno.estado
            return render(request, 'turno_op.html', {'estado_turno': estado_turno, 'turno': turno})
        else:
            return render(request, 'turno_op.html')

    
    def post(self, request):
        if 'action' in request.POST:
            action = request.POST['action']
            turno = TurnoTrabajo.objects.filter(usuario=request.user).first()

            if action == 'iniciar':
                turno.iniciar_turno()
                request.user.disponible = False

            elif action == 'finalizar':
                turno.cerrar_turno()
                request.user.disponible = True

        turno.save()
        request.user.save()

        return render(request, 'turno_op.html')


class PerfilView(View):
    def get(self, request):
        return render(request, 'perfil.html')
    
    def post(self, request):
        logout(request)
        return redirect('index')


class CreacionTurnoView(View):

    def get(self, request):
        operadores = Usuario.objects.filter(permisos=False)
        casillas = Casilla.objects.all()

        return render(request, 'turno.html', {'operadores': operadores, 'casillas': casillas})

    def post(self, request):
        fh_inicio = request.POST['fh_inicio']
        fh_fin = request.POST['fh_fin']
        sentido_cobro = request.POST['direccion']
        monto_inicial = request.POST['monto_inicial']
        casilla = request.POST['select_casilla_id']
        operador_id = request.POST['select_operador_id']

        fecha_inicio = timezone.make_aware(datetime.datetime.strptime(fh_inicio, '%Y-%m-%dT%H:%M'))
        fecha_fin = timezone.make_aware(datetime.datetime.strptime(fh_fin, '%Y-%m-%dT%H:%M'))

        duracion_turno = (fecha_fin - fecha_inicio).total_seconds() / 3600

        if fecha_inicio > fecha_fin:
            messages = "La fecha de inicio no puede ser mayor que la fecha de finalización."
        elif duracion_turno > 9:
            messages = "El turno no puede durar más de 9 horas."
        elif fecha_inicio == fecha_fin:
            messages = "La fecha de inicio no puede ser igual a la fecha de finalización."
        elif casilla == "Seleccione una opción:" or operador_id == "Seleccione una opción:":
            messages = "Debe seleccionar una casilla y un operador."
        else:
            operador_obj = Usuario.objects.get(id=operador_id)
            operador_obj.disponible = False
            operador_obj.save()

            messages = "Turno creado correctamente."

            turno = TurnoTrabajo(
                fh_inicio=fh_inicio,
                fh_fin=fh_fin,
                sentido_cobro=sentido_cobro,
                monto_inicial=monto_inicial,
                enlace_reporte='NULL',
                estado=True,
                casilla_id=casilla,
                usuario_id=operador_id
            )

            turno.save()
        
        return render(request, 'turno.html', {'messages': messages})


class OperadorView(View):
    template_name = 'operador.html'

    def get(self, request):
        usuario = request.user
        turno = TurnoTrabajo.objects.filter(usuario=usuario).first()

        if turno:
            return render(request, self.template_name, {'turno': turno})
        else:
            return render(request, self.template_name)

        
    def post(self, request):
        
        categoria = request.POST['categoria']
        precio = request.POST['precio']
        argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
        fecha = datetime.datetime.now(argentina_timezone).date()

        tarifa = Tarifa(
            categoria = categoria,
            monto = precio,
            fecha_modificacion = fecha
        )

        tarifa.save()

        tarifa_id = tarifa.id

        parametros = {
            'categoria': categoria,
            'precio': precio,
            'tarifa': tarifa_id
        }


        qr_text = f'La categoria del vehiculo es {categoria}, el monto fue de ${precio} y se realizo en la fecha: {fecha}'
        codigo_qr = qrcode.QRCode(
            version=1, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=10,
            border=0,
        )

        codigo_qr.add_data(qr_text)
        codigo_qr.make(fit=True)

        qr_svg = codigo_qr.make_image(fill_color="black", back_color="white")

        nombre_archivo = "qr-code.png"
        ruta_de_guardado = os.path.join('peajeApp', 'static', 'img', nombre_archivo)

        qr_svg.save(ruta_de_guardado)


        return render(request, self.template_name, {'parametros': parametros})


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            if user.permisos == True:
                return redirect('turno')
            else:
                return redirect('operador')
        else:
            return render(request, self.template_name, {'error_message': 'Credenciales inválidas'})


class CreacionEmpleadoView(View):
    def get(self, request):
        return render(request, 'creacion_empleado.html')

    def post(self, request):
        nombre = request.POST['nombre-empleado']
        apellido = request.POST['apellido-empleado']
        username = request.POST['username-empleado']
        direccion = request.POST['direccion-empleado']
        correo = request.POST['email-empleado']
        tipo_documento = request.POST['tipo-documento-empleado']
        nro_documento = request.POST['nro-documento-empleado']
        pass_empleado = request.POST['pass-empleado']

        existe_mail = Usuario.objects.filter(email=correo).exists()
        existe_documento = Usuario.objects.filter(numero_documento=nro_documento).exists()

        if existe_mail:
            error_message = "El correo electrónico ya existe. Por favor, escriba los datos correctamente."
        elif existe_documento:
            error_message = "El número de documento ya existe. Por favor, escriba los datos correctamente."
        else:
            try:
                hashed_password = make_password(pass_empleado)
                empleado = Usuario.objects.create(
                    nombre=nombre,  
                    apellido=apellido,
                    username=username,
                    direccion=direccion,
                    email=correo,
                    tipo_documento=tipo_documento,
                    numero_documento=nro_documento,
                    password=hashed_password,  
                    permisos=False
                )

                error_message = "Empleado creado correctamente."
                return render(request, 'creacion_empleado.html', {'error_message': error_message})
            except IntegrityError:
                error_message = "Ocurrió un error al crear el empleado. Por favor, revise los datos ingresados."


class PanelView(View):
    def get(self, request):
        casillas = Casilla.objects.all()
        return render(request, 'panel_admin.html', {'casillas': casillas})