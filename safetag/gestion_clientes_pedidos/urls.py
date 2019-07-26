from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_autogestion'),
    path('alta_solicitud_presupuesto', views.alta_solicitud_presupuesto, name='alta_sp')
]