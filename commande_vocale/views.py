import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

ESP32_BASE_URL = os.getenv('ESP32_IP', 'http://192.168.43.49')

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def control_led(request):
    if request.method != 'GET':
        return JsonResponse({'erreur': 'Méthode non autorisée'}, status=405)
    
    lamp = request.GET.get('lamp')      # 'salon' ou 'chambre'
    action = request.GET.get('action')  # 'on' ou 'off'
    
    if lamp not in ['salon', 'chambre'] or action not in ['on', 'off']:
        return JsonResponse({'erreur': 'Paramètres invalides'}, status=400)
    
    url = f"{ESP32_BASE_URL}/{lamp}/{action}"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            return JsonResponse({'statut': 'succès', 'message': f"{lamp} {action}"})
        else:
            return JsonResponse({'erreur': f"ESP32 a répondu {r.status_code}"}, status=500)
    except Exception as e:
        return JsonResponse({'erreur': f"ESP32 injoignable : {str(e)}"}, status=500)