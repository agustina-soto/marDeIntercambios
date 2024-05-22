from django.shortcuts import render

def home(request): # cuando un cliente realice una consulta sobre la url "home", se va a ejecutar esta funcion :)
    return render(request, 'home.html', {
        
    })