from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_autogestion'),
    path('alta_solicitud_presupuesto', views.alta_solicitud_presupuesto, name='alta_sp'),
    path('ajax/load-relaciones/', views.carga_relaciones, name='material_ddl'),
    path('thanks', views.thankyoupage, name='thankyou'),

]