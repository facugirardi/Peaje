from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='index'),
    path('turno/', views.CreacionTurnoView.as_view(), name='turno'),
    path('operador/', views.operador, name='operador'),
    path('creacion_empleado/', views.CreacionEmpleadoView.as_view(), name='creacion_empleado'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('perfil/', views.PerfilView.as_view(), name='perfil')
]