import qrcode
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseBadRequest

def contador(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        
        if not nombre or not edad:
            return HttpResponseBadRequest("Por favor, ingresa ambos campos.")

        current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        return redirect('generar_qr', nombre=nombre, edad=edad, current_time=current_time)
    
    return render(request, 'contador.html')

def generar_qr(request, nombre, edad, current_time):
    data = f"Nombre: {nombre}, Edad: {edad}, Hora: {current_time}"
    
    # Generar QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar QR
    qr_filename = f"{current_time.replace(':', '-')}.png"
    qr_path = os.path.join(settings.MEDIA_ROOT, 'qrs', qr_filename)
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    img.save(qr_path)
    
    return render(request, 'ver_qr.html', {'qr_filename': qr_filename, 'data': data})

