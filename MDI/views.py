from django.shortcuts import render

def home(request):
    
    usuario_actual = request.user
    
    context = {
        'usuario': usuario_actual,
        # no se qué pasar
    }

    return render(request, 'home.html', context)
