import requests
import sys
import json
from datetime import date, datetime

if(len(sys.argv) < 4):
    print("Error: provide arguments")
    print("Usage: python otp_bank2ynab_csv.py <date_from> <date_to> <auth_token>")
    print("Example: python otp_bank2ynab_csv.py 2020-09-01 2020-10-01 zzHHJjmss")
    exit(1)


auth_token = sys.argv[3]
date_from = sys.argv[1]
date_to = sys.argv[2]

page_size = 1000

print('Requesting list of operations...')

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru',
    'Authorization': auth_token,
    'Host': 'online.otpbank.ru',
    'Origin': 'https://online.otpbank.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://online.otpbank.ru/dashboard',
}

data = f'{{"data":{{"page":1,"pageSize":{page_size},"dateType":"period","category":null,"sumFrom":0,"sumTo":"","productId":null,"word":"","dateFrom":"{date_from}","dateTo":"{date_to}","operationCategoryId":null}},"accessToken":"{auth_token}"}}'

print('Getting data...')

response = requests.post(
    'https://online.otpbank.ru/v1/user/operation/list', headers=headers, data=data).json()

operation_list = response["data"]["userOperationList"]

print('Writing to file...')

with open("ynab.csv", "w", encoding='utf-8') as f:
    f.write("Date,Payee,Memo,Amount\n")

    for operation in operation_list:
        f.write(datetime.strptime(
            operation["dt"][:10], "%Y-%m-%d").strftime("%d/%m/%Y") + ",")

        f.write((operation["merchantName"] or "None") + ",")

        descr = operation["description"]
        if descr is None:
            descr = ""

        f.write("[{0}]: {1},".format(
            operation["merchantName"] or operation["nomination"].replace(",","_"), descr.replace(",", "_")))

        f.write(operation["operation"]["amount"])

        f.write('\n')


print('Done.')

print('--- TOTAL OPERATIONS ---')
print(len(operation_list))
