from django.shortcuts import render

def base(request):
    return render(request, 'bexp/base.html', {'name': 'Mack'})
