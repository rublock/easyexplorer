from django.shortcuts import render

def base(request):
    
    return render(request, 'base.html')

def address(request):
    address = request.GET.get('address')
    return render(request, 'address_container.html', {'data': address})

