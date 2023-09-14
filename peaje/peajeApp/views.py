from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
def base(request):
    return render(request, 'base.html')


def creacionTurno(request):
    return render(request, 'turno.html')


def operador(request):
    return render(request, 'operador.html')


def login(request):
    return render(request, 'login.html')

def creacion_empleado(request):
    return render(request, 'creacion_empleado.html')