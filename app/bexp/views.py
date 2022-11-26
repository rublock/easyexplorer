from django.shortcuts import render
from blockcypher import get_address_details


def test():
    list = [1, 2, 3, 4, 5]
    for i in list:
        print(i)

test()

def base(request):
    return render(request, 'base.html')



try:
    address_details = get_address_details('34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo')
except AssertionError as error:
    print('Отсутствует адрес', error)
# список из словарей только с транзакциями <class 'list'>
transactions_list = address_details['txrefs']

tempList = []
txrefs_assembler = []  # список без повторяющихся хэшей

for i in transactions_list:
    if i['tx_hash'] in tempList:  # повторяет повторяющиеся хэши и если есть повтор суммирует 'value'
        txrefs_assembler[tempList.index(i['tx_hash'])]['value'] += i['value']
    else:
        tempList.append(i['tx_hash'])
        txrefs_assembler.append(i)

print(txrefs_assembler)

# вывод данных в консоль
for i in txrefs_assembler:
    # tx_hash = i['tx_hash']
    # value = i['value']
    # tx_input_n = i['tx_input_n']
    # confirmed = i['confirmed']
    # confirmations = i['confirmations']
    if i['tx_input_n'] > 0:
        minus_value = 0 - i['value']
        confirmed = i['confirmed'].strftime("%d.%m.%Y %H:%M")
        tx_hash = str(i['tx_hash'])
        value = '{:.8f}'.format(minus_value / 100000000)
        confirmations = str(i['confirmations'])
    else:
        confirmed= i['confirmed'].strftime("%d.%m.%Y %H:%M")
        tx_hash = str(i['tx_hash'])
        value = '{:.8f}'.format(i['value'] / 100000000)
        confirmations = str(i['confirmations'])