from django.shortcuts import render
from django.views.generic import TemplateView
import qrcode
from django.views import View
from django.core.paginator import Paginator
import requests
import json


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"


class AddressView(View):
    def get(self, request):
        blockchair_API = requests.get("https://api.blockchair.com/bitcoin/stats")
        blockchair_data = json.loads(blockchair_API.content)

        error = False

        try:
            user_search = request.GET.get("address")
            address_data = requests.get(
                f"http://127.0.0.1:3002/api/address/{user_search}?limit=9999"
            )
            get_content = address_data._content
            address_data_json = json.loads(get_content)
            api_data = json.dumps(address_data_json["txHistory"])
            address = address_data_json["validateaddress"]["address"]
            tx_num = address_data_json["txHistory"]["txCount"]
        except (AssertionError, IndexError):
            error = True

        if error == True:
            return render(request, "mainapp/base_error.html")
        else:
            balance = address_data_json["txHistory"]["balanceSat"] / 100000000

            # qr = qrcode.QRCode(
            #     box_size=10,
            #     border=6,
            # )
            # qr.add_data(address_data_json["validateaddress"]["address"])

            # img = qr.make_image(fill_color="#F7931A", back_color="white")

            # img.save("static/img/qr.png")

            return render(
                request,
                "mainapp/address.html",
                {
                    "address": address,
                    "api_data": api_data,
                    "balance": balance,
                    "tx_num": tx_num,
                    "blockchair_data": blockchair_data,
                },
            )
