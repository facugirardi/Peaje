from django.urls import path
<<<<<<< HEAD
from .views import *

urlpatterns = [
    path('', index, name = 'admin-main'),
    path('admin/', admin, name="admin-turno"),
    path('detalle/', detalle_usuario, name = 'admin-detalle')
=======
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('turno/', views.creacionTurno, name='turno')
>>>>>>> main
]