from blockcypher import get_address_details
from django.shortcuts import render
from django.views.generic import TemplateView
import qrcode
from django.views import View
import requests
import json


def home(request):
    return render(request, "mainapp/base.html")


def address(request):

    user_search = request.GET.get("address")

    blockchair_API = requests.get("https://api.blockchair.com/bitcoin/stats")
    blockchair_data = json.loads(blockchair_API.content)

    try:

        url = f"https://btcbook.nownodes.io/api/v2/address/{user_search}"

        headers = {
            "api-key": "d688fe5c-4d07-4938-b309-6518ccf352bd",
        }

        get_api_data = requests.get(url, headers=headers)

        if get_api_data.status_code == 200:

            get_api_data.raise_for_status()
            get_content = get_api_data._content
            address_data = json.loads(get_content)

            qr = qrcode.QRCode(
                box_size=10,
                border=6,
            )
            qr.add_data(address_data["address"])
            img = qr.make_image(fill_color="#F7931A", back_color="white")
            img.save("static/img/qr.png")

            address = address_data["address"]
            balance = int(address_data["balance"]) / 100000000
            n_tx = address_data['txs']
            api_data = json.dumps(address_data["txids"])

        else:
            return render(request, "mainapp/base_error.html")

    except Exception as e:
        print(f'server error {str(e)}')


    return render(
        request,
        "mainapp/address.html",
        {
            "address": address,
            "balance": balance,
            "n_tx": n_tx,
            "api_data": api_data,
            "blockchair_data": blockchair_data,
        },
    )