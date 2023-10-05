from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from .models import *
from .models import Usuario

# Create your views here.
def base(request):
    return render(request, 'base.html')



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
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(email=email, password=password)
            request.session['user_id'] = usuario.id
            return redirect('operador')
        except Usuario.DoesNotExist:
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render(request, self.template_name, {'error_message': error_message})


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


        empleado = Usuario(nombre=nombre, 
                           apellido=apellido, 
                           direccion=direccion,
                           email=correo, 
                           tipo_documento=tipo_documento,
                           numero_documento=nro_documento,
                           password=pass_empleado,
                           permisos= True
                           )
        
        empleado.save()

        return render(request, 'creacion_empleado.html')


# Creacion Empleado, Login y Creacion Turno
