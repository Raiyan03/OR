from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api.utils import generateSchTable, getSchedule
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
        emp = data.get('employees')
        print(emp)
        shift = data.get('shifts')
        print(shift)
        shiftTable = generateSchTable(emp, shift)
        schedule = getSchedule(emp, shift, shiftTable)
        # print(schedule)
        # print(shiftTable)
        return JsonResponse({
            'response': 'Data sent succesfyully',
            'data' : schedule,
        })
    except:
        print("Error occured")