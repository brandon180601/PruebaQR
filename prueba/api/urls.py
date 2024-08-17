# urls.py en tu aplicación (por ejemplo, api/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contador, name='contador'),
    path('generar-qr/', views.generar_qr, name='generar_qr'),
    path('generar-pdf/', views.generate_pdf, name='generar_pdf'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    
]
