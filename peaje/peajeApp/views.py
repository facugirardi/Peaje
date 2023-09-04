from django.shortcuts import render
from django.http import HttpResponse
from peajeApp.models import *

# Create your views here.
def index(request):
    return render(request, 'base.html')


def creacionTurno(request):
    if request.method == 'POST':
        id_casilla = request.POST.get('idcasilla')
        id_operador = request.POST.get('idoperador')
        fh_inicio = request.POST.get('fh-incio')
        fh_fin = request.POST.get('fh-fin')
        monto_inicial = request.POST.get('monto-inicial')
        direccion = request.POST.get('direccion')

        casilla_obj = Casilla.objects.get(pk=id_casilla)
        operador_obj = Usuario.objects.get(pk=id_operador)

        # Crea el turno con los objetos relacionados
        turno = TurnoTrabajo(casilla=casilla_obj, usuario=operador_obj, fh_inicio=fh_inicio, fh_fin=fh_fin, monto_inicial=monto_inicial, sentido_cobro=direccion)
        turno.save()

    return render(request, 'turno.html')


def operador(request):
    return render(request, 'operador.html')
