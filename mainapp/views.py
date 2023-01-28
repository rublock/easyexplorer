from blockcypher import get_address_details
from django.shortcuts import render
from django.views.generic import TemplateView
import qrcode
from django.views import View
import requests
import json


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"


class AddressView(View):
    def get(self, request):

        user_search = request.GET.get("address")

        blockchair_API = requests.get("https://api.blockchair.com/bitcoin/stats")
        blockchair_data = json.loads(blockchair_API.content)

        error = False

        try:
            """
            https://blockchain.info/rawaddr/$bitcoin_address
            Address can be base58 or hash160
            Optional limit parameter to show n transactions e.g. &limit=50 (Default: 50, Max: 50)
            Optional offset parameter to skip the first n transactions e.g. &offset=100 (Page 2 for limit 50)
            """
            get_api_data = requests.get(
                f"https://blockchain.info/rawaddr/{user_search}?limit=9999"
            )
            get_content = get_api_data._content
            single_address_data = json.loads(get_content)
        except (AssertionError, IndexError):
            error = True

        if error == True:
            return render(request, "mainapp/base_error.html")
        else:
            qr = qrcode.QRCode(
                box_size=10,
                border=6,
            )
            qr.add_data(single_address_data["address"])
            img = qr.make_image(fill_color="#F7931A", back_color="white")
            img.save("static/img/qr.png")

            address = single_address_data["address"]
            n_tx = single_address_data["n_tx"]
            balance = single_address_data["final_balance"] / 100000000

            tx_data_json = json.dumps(single_address_data["txs"])

            return render(
                request,
                "mainapp/address.html",
                {
                    "address": address,
                    "balance": balance,
                    "n_tx": n_tx,
                    "tx_data_json": tx_data_json,
                    "blockchair_data": blockchair_data,
                },
            )
