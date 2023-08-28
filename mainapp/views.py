from django.shortcuts import render
import qrcode
import requests
import json
from django.core.paginator import Paginator


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
            api_data_temp = address_data["txids"]
            api_data = []

            for i in api_data_temp:
                api_key = "d688fe5c-4d07-4938-b309-6518ccf352bd"
                url = f"https://btcbook.nownodes.io/api/v2/tx/{i}"
                headers = {"api-key": api_key}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()


                    arr_temp = []
                    
                    arr_temp.append(data['blockTime'])
                    arr_temp.append(data['txid'])

                    if data['vin'][0]['addresses'][0] == address:
                        minusValue = 0
                        for j in range(len(data['vout'])):
                            if data['vout'][j]['addresses'][0] != address:
                                minusValue -= int(data['vout'][j]['value'])
                        arr_temp.append(round((minusValue - int(data['fees'])) / 100000000, 8))
                    else:
                        for j in range(len(data['vout'])):
                            if data['vout'][j]['addresses'][0] == address:
                                arr_temp.append(round(int(data['vout'][j]['value']) / 100000000, 8))
                    api_data.append(arr_temp)

                else:
                    print("Произошла ошибка при выполнении запроса.")

            paginator = Paginator(api_data, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

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
            "page_obj": page_obj,
        },
    )