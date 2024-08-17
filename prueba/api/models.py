from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class Usuario(models.Model):
    # Campos de información personal
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correo_electronico = models.EmailField(unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Opciones de servicio
    OPCIONES_SERVICIO = [
        ('SS', 'Servicio Social'),
        ('R', 'Residencias'),
    ]
    tipo_servicio = models.CharField(max_length=2, choices=OPCIONES_SERVICIO)

    # Horas realizadas
    horas_realizadas = models.IntegerField(default=0)  # Se actualizará según las horas realizadas
    horas_requeridas = models.IntegerField()  # Horas requeridas para el servicio

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    def save(self, *args, **kwargs):
        if self.tipo_servicio == 'SS':
            self.horas_requeridas = 480
        elif self.tipo_servicio == 'R':
            self.horas_requeridas = 500
        super().save(*args, **kwargs)

    @property
    def fecha_estimada_conclusion(self):
        dias_necesarios = (self.horas_requeridas - self.horas_realizadas) / 4  # Asumiendo 4 horas por día
        return self.fecha_registro + timedelta(days=dias_necesarios)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Usuario, TipoUsuario
from django.http import HttpResponse

@login_required
def usuario_create(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        correo_electronico = request.POST.get('correo_electronico')
        tipo_usuario_id = request.POST.get('tipo_usuario')
        estatus = request.POST.get('estatus')

        tipo_usuario = TipoUsuario.objects.get(pk=tipo_usuario_id)

        # Crear el usuario
        Usuario.objects.create(
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo_electronico=correo_electronico,
            tipo_usuario=tipo_usuario,
            estatus=estatus
        )
        return redirect('usuario_list')
    
    tipo_usuarios = TipoUsuario.objects.all()
    return render(request, 'asistencias/usuario_form.html', {'tipo_usuarios': tipo_usuarios})