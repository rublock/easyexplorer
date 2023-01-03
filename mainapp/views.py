from blockcypher import get_address_details
from django.shortcuts import render
from django.views.generic import TemplateView
import qrcode
from django.views import View
from django.core.paginator import Paginator


class MainPageView(TemplateView):
    template_name = "mainapp/base.html"

class AddressView(View):

    def get(self, request):
        address_details = get_address_details(request.GET.get('address'), txn_limit=9999)
        temp_list = []
        temp_array = []
        data = {}
        count = 0
        balance = address_details['balance'] / 100000000


        qr = qrcode.QRCode(
            box_size=10,
            border=6,
        )
        qr.add_data(address_details['address'])

        img = qr.make_image(fill_color="#F7931A", back_color="white")

        img.save("static/img/qr.png")

        for i in address_details['txrefs']:
            if i['tx_hash'] in temp_list:
                temp_array[temp_list.index(i['tx_hash'])]['value'] += i['value']
            else:
                temp_list.append(i['tx_hash'])
                temp_array.append(i)

        for i in temp_array:
            if i['tx_input_n'] > 0:
                minus_value = 0 - i['value']
                data[count] = [
                    (i['confirmed'].strftime("%d.%m.%Y %H:%M")),
                    (i['tx_hash']),
                    (minus_value / 100000000)
                ]
                count += 1
            else:
                data[count] = [
                    (i['confirmed'].strftime("%d.%m.%Y %H:%M")),
                    (i['tx_hash']),
                    (i['value'] / 100000000)
                ]
                count += 1

        pag = Paginator(data, 10)
        pag_list = [*range(pag.num_pages)]

        return render(request, 'mainapp/address.html', {'address_details': address_details,'balance': balance, 'data': data, 'pag_list': pag_list})