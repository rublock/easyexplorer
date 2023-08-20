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

        try:
            get_api_data = requests.get(f"https://blockchain.info/rawaddr/{user_search}?limit=9999")

            if get_api_data.status_code == 200:

                get_api_data.raise_for_status()
                get_content = get_api_data._content
                single_address_data = json.loads(get_content)

                qr = qrcode.QRCode(
                    box_size=10,
                    border=6,
                )
                qr.add_data(single_address_data["address"])
                img = qr.make_image(fill_color="#F7931A", back_color="white")
                img.save("static/img/qr.png")

                address = single_address_data["address"]
                balance = single_address_data["final_balance"] / 100000000

                api_data = []

                for i in range(len(single_address_data['txs'])):
                    dict = {}
                    dict[0] = single_address_data['txs'][i]['hash']
                    dict[1] = single_address_data['txs'][i]['time']
                    dict[2] = single_address_data['txs'][i]['result'] / 100000000
                    api_data.append(dict)

                n_tx = len(api_data)
                api_data = json.dumps(api_data)

            else:
                return render(request, "mainapp/base_error.html")

        except Exception as e:

            try:
                address_data = requests.get(f"http://127.0.0.1:3002/api/address/{user_search}?limit=9999")

                status = json.loads(address_data.text)

                if 'txHistory' in status:
                    get_content = address_data.text
                    address_data_json = json.loads(get_content)

                    qr = qrcode.QRCode(
                        box_size=10,
                        border=6,
                    )
                    qr.add_data(address_data_json["validateaddress"]["address"])
                    img = qr.make_image(fill_color="#F7931A", back_color="white")
                    img.save("static/img/qr.png")

                    address = address_data_json["validateaddress"]["address"]
                    balance = address_data_json["txHistory"]["balanceSat"] / 100000000
                    n_tx = address_data_json['txHistory']['txCount']

                    api_data = json.dumps(address_data_json["txHistory"])
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