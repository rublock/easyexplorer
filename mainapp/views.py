from django.shortcuts import render
import qrcode
import requests
import json
from django.core.paginator import Paginator
from datetime import datetime


def home(request):
    return render(request, "mainapp/base.html")


def address(request):

    user_search = request.GET.get("address")

    blockchair_API = requests.get("https://api.blockchair.com/bitcoin/stats")
    blockchair_data = json.loads(blockchair_API.content)
    market_price_usd = blockchair_data['data']['market_price_usd']

    try:

        url = f"https://btcbook.nownodes.io/api/v2/address/{user_search}"

        headers = {
            "api-key": "d688fe5c-4d07-4938-b309-6518ccf352bd",
        }

        nownodes_getaddress = requests.get(url, headers=headers)

        if nownodes_getaddress.status_code == 200:

            nownodes_getaddress.raise_for_status()
            nownodes_getaddress_content = nownodes_getaddress._content
            nownodes_getaddress_json = json.loads(nownodes_getaddress_content)

            qr = qrcode.QRCode(
                box_size=10,
                border=6,
            )
            qr.add_data(nownodes_getaddress_json["address"])
            img = qr.make_image(fill_color="#F7931A", back_color="white")
            img.save("static/img/qr.png")

            address = nownodes_getaddress_json["address"]
            balance = int(nownodes_getaddress_json["balance"]) / 100000000
            txs = nownodes_getaddress_json['txs']

            txids = nownodes_getaddress_json["txids"]

            paginator = Paginator(txids, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            for i in range(len(page_obj.object_list)):
                page_obj.object_list[i] = [page_obj.object_list[i]]

            url = ''

            for i in range(10): #исправить

                if page_number:
                    slice_two = int(page_number) * 10
                    slice_one = slice_two - 10
                    url = f"https://btcbook.nownodes.io/api/v2/tx/{txids[slice_one:slice_two][i]}"
                else:
                    url = f"https://btcbook.nownodes.io/api/v2/tx/{txids[0:10][i]}"

                api_key = "d688fe5c-4d07-4938-b309-6518ccf352bd"

                headers = {
                    "api-key": api_key
                }

                nownodes_gettransaction = requests.get(url, headers=headers)

                if nownodes_gettransaction.status_code == 200:
                    nownodes_gettransaction_json = nownodes_gettransaction.json()

                    confirmations = nownodes_gettransaction_json['confirmations']

                    date_time_human = datetime.utcfromtimestamp(nownodes_gettransaction_json['blockTime']).strftime('%d.%m.%Y %H:%M')
                    
                    page_obj.object_list[i].append(date_time_human)

                    if nownodes_gettransaction_json['vin'][0]['addresses'][0] == address:
                        minusValue = 0
                        for j in range(len(nownodes_gettransaction_json['vout'])):
                            if nownodes_gettransaction_json['vout'][j]['addresses'][0] != address:
                                minusValue -= int(nownodes_gettransaction_json['vout'][j]['value'])
                        minusValue -= int(nownodes_gettransaction_json['fees'])
                        page_obj.object_list[i].append(minusValue / 100000000)
                    else:
                        for j in range(len(nownodes_gettransaction_json['vout'])):
                            if nownodes_gettransaction_json['vout'][j]['addresses'][0] == address:
                                page_obj.object_list[i].append(round(int(nownodes_gettransaction_json['vout'][j]['value']) / 100000000, 8))
                    
                    page_obj.object_list[i].append(confirmations)

                else:
                    print("Произошла ошибка при выполнении запроса.")

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
            "txs": txs,
            "market_price_usd": market_price_usd,
            "page_obj": page_obj,
            "confirmations": confirmations,
        },
    )