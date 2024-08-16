from django.urls import path
from . import views

urlpatterns = [
    path('', views.contador, name='contador'),
    path('generar-qr/<str:nombre>/<int:edad>/<str:current_time>/', views.generar_qr, name='generar_qr'),
]