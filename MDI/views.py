# from django.http import HttpResponse # permite responder a una peticion de un cliente
from django.shortcuts import render

def home(request): # cuando un cliente realice una consulta sobre la url "home", se va a ejecutar esta funcion :)
    return render(request, 'home.html', {
        #context
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #diccionario
        password = request.POST.get('password') #diccionario
        
    return render(request, 'login.html', {
        #context
    })

def prueba(request):
    return render(request, 'prueba.html')

def prueba2(request):
    return render(request, 'prueba2.html')
