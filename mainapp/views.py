from django.shortcuts import render
from blockcypher import get_address_details
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"