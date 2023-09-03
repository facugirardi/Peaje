from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'base.html')

<<<<<<< HEAD
def detalle_usuario(request):
    return render(request, 'detalle.html')

def admin(request):
    return render(request, 'admin.html')
=======
def creacionTurno(request):
    return render(request, 'turno.html')