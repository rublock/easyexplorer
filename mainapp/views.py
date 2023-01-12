from blockcypher import get_address_details
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

        blockchair_API = requests.get('https://api.blockchair.com/bitcoin/stats')
        blockchair_data = json.loads(blockchair_API.content)

        address_details = get_address_details(
            request.GET.get("address"), txn_limit=9999
        )
        temp_list = []
        temp_array = []
        tx_data = []
        count = 0
        balance = address_details["balance"] / 100000000

        qr = qrcode.QRCode(
            box_size=10,
            border=6,
        )
        qr.add_data(address_details["address"])

        img = qr.make_image(fill_color="#F7931A", back_color="white")

        img.save("static/img/qr.png")

        for i in address_details["txrefs"]:
            if i["tx_hash"] in temp_list:
                temp_array[temp_list.index(i["tx_hash"])]["value"] += i["value"]
            else:
                temp_list.append(i["tx_hash"])
                temp_array.append(i)

        for i in temp_array:
            if i["tx_input_n"] > 0:
                minus_value = 0 - i["value"]
                tx_data.append([i["confirmed"].strftime("%d.%m.%Y %H:%M"), i["tx_hash"], (minus_value / 100000000)])
                count += 1
            else:
                tx_data.append([i["confirmed"].strftime("%d.%m.%Y %H:%M"), i["tx_hash"], (i["value"] / 100000000)])
                count += 1

        paginator = Paginator(tx_data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "mainapp/address.html",
            {
                "address_details": address_details,
                "balance": balance,
                "tx_data": tx_data,
                "page_obj": page_obj,
                "blockchair_data": blockchair_data,
            },
        )
