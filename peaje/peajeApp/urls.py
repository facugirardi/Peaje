from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='index'),
    path('turno/', views.CreacionTurnoView.as_view(), name='turno'),
    path('operador/', views.OperadorView.as_view(), name='operador'),
    path('creacion_empleado/', views.CreacionEmpleadoView.as_view(), name='creacion_empleado'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('navbar/', views.navbar, name='navbar'),
    path('ticket/', views.ticket_view, name='ticket'),
    path('gestion_turno/', views.GestionTurnoView.as_view(), name='gestion_turno'),
    path('panel/', views.PanelView.as_view(), name='panel'), 
]