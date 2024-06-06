import requests
import csv

CURRENCY_CODE = 'USD' # Set to supported currency code from ISO 4217 https://www.iso.org/iso-4217-currency-codes.html 

# Get List Prices in the same currency as the rate card and structure as a map for fast querying
api_url = 'https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?'
list_prices = requests.get(api_url + "&currencyCode=" + CURRENCY_CODE)
list_prices.raise_for_status()
list_prices = list_prices.json()['items']

if len(list_prices) <= 0:
    raise('No data returned')

column_headers = []
for i in list_prices:
    
    ccl = i['currencyCodeLocalizations'][0]
    prices = ccl['prices'][0]
    i['currencyCode'] = ccl["currencyCode"]
    i['model'] = prices['model']
    i['value'] = prices['value']
    del i['currencyCodeLocalizations']

    for k in i.keys():
        if k not in column_headers:
            column_headers.append(k)


with open('public_sku_list.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=column_headers)
    writer.writeheader()
    writer.writerows(list_prices)