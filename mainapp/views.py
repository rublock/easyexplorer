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

        blockchair_API = requests.get('https://api.blockchair.com/bitcoin/stats')
        blockchair_data = json.loads(blockchair_API.content)

        error = False

        try:
            address_details = get_address_details(
                # get data from <input name="address" /> base.html
                request.GET.get("address"), txn_limit=9999
            )
        except (AssertionError, IndexError):
            error = True

        if error == True:
            return render(request, 'mainapp/base_error.html')
        else:
            temp_list = []
            temp_array = []
            dict = {}
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
                temp_dict = {}
                if i["tx_input_n"] >= 0:
                    minus_value = 0 - i["value"]
                    temp_dict[0] = i["tx_hash"]
                    temp_dict[1] = i["confirmed"].strftime("%d.%m.%Y %H:%M")
                    temp_dict[2] = minus_value / 100000000
                    dict[count] = temp_dict
                    count += 1
                else:
                    temp_dict[0] = i["tx_hash"]
                    temp_dict[1] = i["confirmed"].strftime("%d.%m.%Y %H:%M")
                    temp_dict[2] = i["value"] / 100000000
                    dict[count] = temp_dict
                    count += 1

            tx_data_json = json.dumps(dict)

            return render(
                request,
                "mainapp/address.html",
                {
                    "address_details": address_details,
                    "balance": balance,
                    "tx_data_json": tx_data_json,
                    "blockchair_data": blockchair_data,
                },
            )

