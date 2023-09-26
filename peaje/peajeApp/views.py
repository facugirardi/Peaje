from django.shortcuts import render
from django.views.generic import ListView
from .models import *

# Create your views here.
def base(request):
    return render(request, 'base.html')


def creacionTurno(request):

    operadores = Usuario.objects.all()
    casillas = Casilla.objects.all()    

    return render(request, 'turno.html', {'operadores': operadores, 'casillas': casillas})


def operador(request):
    return render(request, 'operador.html')


def login(request):
    return render(request, 'login.html')

def creacion_empleado(request):
    if request.method == 'POST':
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
