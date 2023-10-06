from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import *
from .models import Usuario 
from django.utils import timezone 
from datetime import datetime
from .models import Usuario
from django.contrib.auth import logout, login, authenticate

def base(request):
    return render(request, 'base.html')


class PerfilView(View):
    def get(self, request):
        return render(request, 'perfil.html')
    
    def post(self, request):
        logout(request)
        return redirect('index')


class CreacionTurnoView(View):

    def get(self, request): 
        operadores = Usuario.objects.all()
        casillas = Casilla.objects.all()

        return render(request, 'turno.html', {'operadores': operadores, 'casillas': casillas})



    def post(self, request):
        fh_inicio = request.POST['fh_inicio']
        fh_fin = request.POST['fh_fin']
        sentido_cobro = request.POST['direccion']
        monto_inicial = request.POST['monto_inicial'] 
        operador = request.POST['select_operador_id']
        casilla = request.POST['select_casilla_id']

        fecha_inicio = timezone.make_aware(datetime.strptime(fh_inicio, '%Y-%m-%dT%H:%M'))
        fecha_fin = timezone.make_aware(datetime.strptime(fh_fin, '%Y-%m-%dT%H:%M'))

        duracion_turno = (fecha_fin - fecha_inicio).total_seconds() / 3600
        
        if fecha_inicio > fecha_fin:
            message = "La fecha de inicio no puede ser mayor que la fecha de finalización."
            return render(request, 'turno.html', {'message': message})
        
        elif duracion_turno > 9:
            message = "El turno no puede durar más de 9 horas."
            return render(request, 'turno.html', {'message': message})

        elif fecha_inicio > fecha_fin and duracion_turno > 9:
            message = "La fecha de inicio no puede ser mayor que la fecha de finalización y el turno no puede durar más de 9 horas."
            return render(request, 'turno.html', {'message': message})
        
        else:
            message = "Turno creado correctamente."
        
        turno = TurnoTrabajo(
            fh_inicio=fh_inicio,
            fh_fin=fh_fin,
            sentido_cobro=sentido_cobro,
            monto_inicial=monto_inicial,
            enlace_reporte='NULL',
            estado=True,
            casilla_id=casilla,
            usuario_id=operador
        )
        
        turno.save()

        return render(request, 'turno.html')



def operador(request):
    return render(request, 'operador.html')


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
        direccion = request.POST['direccion-empleado']
        correo = request.POST['email-empleado']
        tipo_documento = request.POST['tipo-documento-empleado']
        nro_documento = request.POST['nro-documento-empleado']
        pass_empleado = request.POST['pass-empleado']


        existe_mail = Usuario.objects.filter(email=correo).exists()
        existe_documento = Usuario.objects.filter(numero_documento=nro_documento).exists()

        if existe_mail:
            error_message = "El correo electrónico ya existe. Escriba los datos correctamente"
        elif existe_documento:
            error_message = "El número de documento ya existe. Escriba los datos correctamente"
        else:

            empleado = Usuario(nombre=nombre, 
                               apellido=apellido, 
                               direccion=direccion,
                               email=correo, 
                               tipo_documento=tipo_documento,
                               numero_documento=nro_documento,
                               password=pass_empleado,
                               permisos=True)
            empleado.save()
            return render(request, 'creacion_empleado.html')

        return render(request, 'creacion_empleado.html', {'error_message': error_message})


    

# Creacion Empleado, Login y Creacion Turno
