from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def detalle_usuario(request):
    return render(request, 'detalle.html')

def admin(request):
    return render(request, 'admin.html')