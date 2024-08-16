# urls.py en tu aplicación (por ejemplo, api/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contador, name='contador'),
    path('generar-qr/', views.generar_qr, name='generar_qr'),
]
