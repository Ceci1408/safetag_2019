from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alta_cliente', views.alta_cliente, name='alta_cliente'),
    path('cliente/<int:id_cliente>/alta_dato_contacto', views.cliente_alta_dato_contacto, name='cliente_alta_dc'),
    path('cliente/<int:id_cliente>/alta_domicilio', views.cliente_alta_domicilio, name='cliente_alta_domicilio'),

    path('alta_proveedor', views.alta_proveedor, name='alta_proveedor'),
    path('proveedor/<int:id_proveedor>/alta_dato_contacto', views.proveedor_alta_dato_contacto,
         name='proveedor_alta_dc'),
    path('proveedor/<int:id_proveedor>/alta_domicilio', views.proveedor_alta_domicilio,
         name='proveedor_alta_domicilio'),

    path('alta_servicio_tecnico', views.alta_servicio_tecnico, name='alta_servicio_tecnico'),
    path('servicio_tecnico/<int:id_service>/alta_dato_contacto', views.service_alta_dato_contacto, name='st_alta_dc'),
    path('servicio_tecnico/<int:id_service>/alta_domicilio', views.service_alta_domicilio, name='st_alta_domicilio'),


]