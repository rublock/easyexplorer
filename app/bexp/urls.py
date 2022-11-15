from django.urls import path
from .views import *
from django.contrib import admin

urlpatterns = [
    path('admin', admin.site.urls),
    path('', base),
    path('address', address)
]
