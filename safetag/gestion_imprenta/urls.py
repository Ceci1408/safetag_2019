from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alta_tipo_cliente', views.alta_tipo_cliente, name='alta_tipo_cliente'),
    path('alta_cliente', views.alta_cliente, name='alta_cliente'),
    path('cliente/<int:id_cliente>/alta_domicilio', views.cliente_alta_domicilio, name='cliente_alta_domicilio'),
    path('proveedor/<int:id_proveedor>/alta_domicilio', views.proveedor_alta_domicilio,
         name='proveedor_alta_domicilio'),
    path('alta_pais', views.alta_pais, name='alta_pais'),
    path('alta_provincia', views.alta_provincia, name='alta_provincia'),
    path('alta_localidad', views.alta_localidad, name='alta_localidad'),
    path('cliente/<int:id_cliente>/alta_dato_contacto', views.cliente_alta_dato_contacto, name='cliente_alta_dc'),
    path('proveedor/<int:id_proveedor>/alta_dato_contacto', views.proveedor_alta_dato_contacto,
         name='proveedor_alta_dc'),
    path('servicio_tecnico/<int:id_service>/alta_dato_contacto', views.cliente_alta_dato_contacto, name='st_alta_dc'),
    path('alta_proveedor', views.alta_proveedor, name='alta_proveedor'),
    path('alta_material', views.alta_material, name='alta_material'),
    path('alta_tipo_trabajo', views.alta_tipo_trabajo, name='alta_tipo_trabajo'),
    path('alta_medida_estandar', views.alta_medida_estandar, name='alta_medida_estandar'),
    path('alta_cantidad', views.alta_cantidad, name='alta_cantidad'),
    path('alta_color_impresion', views.alta_color_impresion, name='alta_color_impresion'),
    path('tipo_trabajo/<int:tipo_trabajo_id>/cantidad', views.tipo_trabajo_cantidad, name='tipo_trabajo_cantidad'),
    path('alta_terminacion', views.alta_terminacion, name='alta_terminacion'),
    path('alta_maquina_terminacion', views.alta_maquina_terminacion, name='alta_maquina_terminacion'),
    path('alta_maquina_pliego', views.alta_maquina_pliego, name='alta_maquina_pliego'),
    path('maquina/<int:maquina_id>/terminacion', views.maquina_terminaciones, name='alta_maq_terminacion'),
    path('maquina/<int:maquina_id>/color', views.maquina_color_impresion, name='maquina_color_impresion')
]