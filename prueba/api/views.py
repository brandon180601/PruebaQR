import qrcode
import base64
from io import BytesIO
from django.shortcuts import render
from django.utils import timezone
import pytz
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

def contador(request):
    # Convertir la hora a la zona horaria local
    local_tz = pytz.timezone('America/Mexico_City')
    local_time = timezone.now().astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    return render(request, 'contador.html', {'current_time': local_time})

def generar_qr(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        
        # Convertir la hora a la zona horaria local
        local_tz = pytz.timezone('America/Mexico_City')
        local_time = timezone.now().astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        # Datos a codificar en el QR
        data = f"Nombre: {nombre}\nEdad: {edad}\nHora: {local_time}"
        
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

        return render(request, 'ver_qr.html', {'qr_code': img_str, 'current_time': local_time})

    return render(request, 'contador.html')

def generate_pdf(request):
    # Renderiza la plantilla HTML
    html = render_to_string('contador.html', {'data': 'tu_dato'})
    
    # Genera el PDF
    pdf_file = HTML(string=html).write_pdf()
    
    # Retorna el PDF como una respuesta HTTP
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mi_archivo.pdf"'
    return response