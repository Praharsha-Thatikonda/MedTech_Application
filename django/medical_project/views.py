from django.shortcuts import render
# Import Database Tools
import sys
import os
try:
    from databases.sql_manager import sql_manager
except ImportError:
    # Path hack for Django
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'databases')))
    try:
        from sql_manager import sql_manager
    except ImportError:
         # Fallback if pathing fails (shouldn't if f_two is root)
         sql_manager = None

def index(request):
    return render(request, 'index.html')

def doctors(request):
    doctors_list = sql_manager.get_all_doctors() if sql_manager else []
    return render(request, 'doctors.html', {'doctors': doctors_list})

def hospitals(request):
    hospitals_list = sql_manager.get_all_hospitals() if sql_manager else []
    return render(request, 'hospitals.html', {'hospitals': hospitals_list})

def ailab(request):
    return render(request, 'ailab.html')

def map_view(request):
    return render(request, 'map.html')

def profile(request):
    return render(request, 'profile.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            
            # LLM Integration Path
            if os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) not in sys.path:
                sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
            
            # Load Data (From Central DB)
            try:
                doctors = sql_manager.get_all_doctors() if sql_manager else []
                hospitals = sql_manager.get_all_hospitals() if sql_manager else []
            except:
                doctors = []
                hospitals = []
                
            data_context = {
                'doctors': doctors,
                'hospitals': hospitals,
                'user_coords': data.get('coords')
            }
            
            from llm_service import llm_service
            model_key = data.get('model', 'gemma-it')
            reply = llm_service.generate_response(text, model_key=model_key, context=data_context)
            
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'reply': f"Error: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def transportation(request):
    return render(request, 'transportation.html')
