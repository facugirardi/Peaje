from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'admin-main'),
    path('admin/', admin, name="admin-turno"),
    path('detalle/', detalle_usuario, name = 'admin-detalle')
]