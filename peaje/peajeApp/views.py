
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
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
from config.forms import CasillasFilterForm
from datetime import date
from decimal import Decimal


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
    turno = TurnoTrabajo.objects.filter(usuario=usuario).last()

    if turno:
        return render(request, 'ticket.html',  {'fecha': fecha, 'hora': hora, 'turno': turno})
    else:
        return render(request, 'ticket.html',  {'fecha': fecha, 'hora': hora})


class GestionTurnoView(View):
    def get(self, request):

        usuario = request.user
        turno = TurnoTrabajo.objects.filter(usuario=usuario).last()

        if turno:
            estado_turno = turno.estado
            return render(request, 'turno_op.html', {'estado_turno': estado_turno, 'turno': turno})
        else:
            return render(request, 'turno_op.html')

    
    def post(self, request):
        if 'action' in request.POST:
            action = request.POST['action']
            turno = TurnoTrabajo.objects.filter(usuario=request.user).last()

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
        estaciones = Estacion.objects.all()

        return render(request, 'turno.html', {'operadores': operadores, 'casillas': casillas, 'estaciones':estaciones})

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
        turno = TurnoTrabajo.objects.filter(usuario=usuario).last()

        fecha_fin = 0
        fecha_inicio = 0


        if turno:
            fh_fin = str(turno.fh_fin)
            fh_fin = fh_fin.split('+')[0]

            argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')

            fh_inicio = datetime.datetime.now(argentina_timezone)
            fh_inicio = fh_inicio.replace(microsecond=0, tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
            fh_inicio = str(fh_inicio)

            fecha_inicio = datetime.datetime.strptime(fh_inicio, '%Y-%m-%d %H:%M:%S')
            fecha_fin = datetime.datetime.strptime(fh_fin, '%Y-%m-%d %H:%M:%S')

            duracion_turno = (fecha_fin - fecha_inicio).total_seconds() / 60
        
            horas_restantes = int(duracion_turno)
            estado = turno.estado
        else:
            horas_restantes = 0
            estado = False

        print(horas_restantes)

        if horas_restantes < 0:
            horas_restantes = 0
        elif estado == False:
            horas_restantes = 0

        if turno:
            return render(request, self.template_name, {'turno': turno, 'tiempo': horas_restantes})
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
        num_casilla = request.GET.get('num_casilla')
        casillas = Casilla.objects.all()
        if num_casilla:
            casillas = casillas.filter(num_casilla__icontains=num_casilla)
        context = {
            'form': CasillasFilterForm(),
            'casillas' : casillas
        }

        return render(request, 'panel_admin.html', context)
    
class DetalleCasillaView(View):
    template_name = "detalle_casilla.html"

    def get(self, request, casilla_id):
        casilla = get_object_or_404(Casilla, id=casilla_id)
        try:
            turnos_actuales = TurnoTrabajo.objects.filter(casilla_id=casilla_id)
            turno_actual = turnos_actuales.last()

        except TurnoTrabajo.DoesNotExist:
            turno_actual = None

        return render(request, self.template_name, {'casilla': casilla, 'turno_actual': turno_actual})

    def post(self, request, casilla_id):
        casilla = get_object_or_404(Casilla, id=casilla_id)

        if 'abrir_casilla' in request.POST:
            casilla.abrir_casilla()

        if 'cerrar_casilla' in request.POST:
            if not TurnoTrabajo.objects.filter(casilla_id=casilla_id, estado=True).exists():
                casilla.cerrar_casilla()
            else:
                return HttpResponseBadRequest("No puedes cerrar la casilla mientras haya un turno en curso.")

        return render(request, self.template_name, {'casilla': casilla})


def test_view(request):
    turnos = TurnoTrabajo.objects.all()

    return render(request, 'test.html', {'turnos': turnos})


def reporte_view(request, casilla_id):
    argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    fecha = datetime.datetime.now(argentina_timezone).date()
    print(fecha)

    casilla = Casilla.objects.get(id=casilla_id)
    tarifas_hoy = Tarifa.objects.filter(fecha_modificacion__gte=date.today())

    monto_total = Decimal(0)

    cantidad_1 = 0
    monto_total_1 = Decimal(0)

    cantidad_2 = 0
    monto_total_2 = Decimal(0)

    cantidad_3 = 0
    monto_total_3 = Decimal(0)

    cantidad_4 = 0
    monto_total_4 = Decimal(0)

    cantidad_5 = 0
    monto_total_5 = Decimal(0)

    cantidad_6 = 0
    monto_total_6 = Decimal(0)

    cantidad_7 = 0
    monto_total_7 = Decimal(0)

    for tarifa in tarifas_hoy:
        categoria = tarifa.categoria
        monto = tarifa.monto

        monto_total += monto

        if categoria == '1':
            cantidad_1 += 1
            monto_total_1 += monto
        elif categoria == '2':
            cantidad_2 += 1
            monto_total_2 += monto
        elif categoria == '3':
            cantidad_3 += 1
            monto_total_3 += monto
        elif categoria == '4':
            cantidad_4 += 1
            monto_total_4 += monto
        elif categoria == '5':
            cantidad_5 += 1
            monto_total_5 += monto
        elif categoria == '6':
            cantidad_6 += 1
            monto_total_6 += monto
        elif categoria == '7':
            cantidad_7 += 1
            monto_total_7 += monto

    try:
        datos_render = {
            'fecha': fecha,
            'casilla': casilla,
            'monto_total': monto_total,
            'cantidad_1': cantidad_1,
            'monto_total_1': monto_total_1,
            'cantidad_2': cantidad_2,
            'monto_total_2': monto_total_2,
            'cantidad_3': cantidad_3,
            'monto_total_3': monto_total_3,
            'cantidad_4': cantidad_4,
            'monto_total_4': monto_total_4,
            'cantidad_5': cantidad_5,
            'monto_total_5': monto_total_5,
            'cantidad_6': cantidad_6,
            'monto_total_6': monto_total_6,
            'cantidad_7': cantidad_7,
            'monto_total_7': monto_total_7,
        }

        print(datos_render)

        return render(request, 'reporte.html', datos_render)

    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'reporte.html')
    

class PanelTarifasView(View):
    def get(self, request):
        tarifas = Tarifa.objects.all()
        return render(request, 'panel_tarifas.html', {'tarifas': tarifas})
    
class DetalleTarifas(View):
    def get(self, request, tarifa_id):
        tarifa = get_object_or_404(Tarifa, id=tarifa_id)
        return render(request, 'detalle_tarifa.html', {'tarifa': tarifa})
