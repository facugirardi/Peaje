from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='index'),
    path('turno/', views.creacionTurno, name='turno'),
    path('operador/', views.operador, name='operador'),
    path('creacion_empleado/', views.CreacionEmpleadoView.as_view(), name='creacion_empleado'),
    path('login/', views.login, name='login')
]