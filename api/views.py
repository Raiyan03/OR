from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

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

