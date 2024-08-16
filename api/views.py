# views.py
import qrcode
import base64
from io import BytesIO
from django.shortcuts import render
from django.utils import timezone

def contador(request):
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'contador.html', {'current_time': current_time})

def generar_qr(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Datos a codificar en el QR
        data = f"Nombre: {nombre}\nEdad: {edad}\nHora: {current_time}"
        
        # Generar el QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir la imagen a base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return render(request, 'ver_qr.html', {'qr_code': img_str, 'current_time': current_time})

    return render(request, 'contador.html')
