from django.shortcuts import render
from django.http import HttpResponse
from peajeApp.models import Usuario

# Create your views here.
def index(request):
    return render(request, 'index.html')
    #return HttpResponse('usuarios')

def detalle_usuario(request):
    return render(request, 'detalle.html')

def usuario(request):
    usuario = Usuario.objects