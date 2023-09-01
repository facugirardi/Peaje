from django.urls import path
from .views import index, detalle_usuario

urlpatterns= [
    path('', index, name='admin-index'),
    path('detalle/', detalle_usuario, name='admin-detalle'),
]