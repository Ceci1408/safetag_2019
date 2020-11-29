from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_autogestion'),
    path('alta_solicitud_presupuesto', views.alta_solicitud_presupuesto, name='alta_sp'),
    #path('alta_solicitud_terminaciones/<int:solicitud_id>/', views.alta_solicitud_terminaciones, name='alta_sp_term'),
    path('ajax/load-relaciones/', views.carga_material, name='material_ddl'),
]