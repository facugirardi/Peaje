from django.shortcuts import render
from django.http import HttpResponse
from peajeApp.models import *

# Create your views here.
def index(request):
    return render(request, 'base.html')


def creacionTurno(request):
    return render(request, 'turno.html')


def operador(request):
    return render(request, 'operador.html')


def creacion_empleado(request):
    return render(request, 'creacion_empleado.html')