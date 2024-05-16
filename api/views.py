from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

def index(request):
    html = f'''

    <html>
        <body>
            <h1>
                welcome to django
            <h1>
        <body>
    <html>
    '''
    return HttpResponse(html)

def greet(request):
    #Guest incase no params is passed 
    name = request.GET.get('name', 'Guest')
    return JsonResponse({ 'response': name})

@csrf_exempt
@require_http_methods(['POST'])
def schedule(request):
    try:
        data = json.loads(request.body)
        req = data.get('data')
        return JsonResponse({
            'response': 'Data sent succesfyully',
            'data' : req
        })
    except:
        print("Error occured")