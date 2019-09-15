from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_autogestion'),
    path('alta_solicitud_presupuesto/<int:cliente_id>/', views.alta_solicitud_presupuesto, name='alta_sp'),
    path('alta_solicitud_terminaciones/<int:solicitud_id>/', views.alta_solicitud_terminaciones, name='alta_sp_term'),
    path('alta_cliente', views.alta_cliente, name='alta_cliente'),

]