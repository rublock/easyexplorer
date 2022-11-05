from django.shortcuts import render

def base(request):
    return render(request, 'base.html', {'name': 'Mack'})

def search(request):
    return render(request, 'search.html')
