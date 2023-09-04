from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('turno/', views.creacionTurno, name='turno'),
    path('operador/', views.operador, name='operador')
]