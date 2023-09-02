from django.urls import path
from .views import index, detalle_usuario

urlpatterns = [
    path('', index, name = 'admin-main'),
    path('detalle/', detalle_usuario, name = 'admin-detalle'),
]