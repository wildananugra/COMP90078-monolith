import requests

token = "http://localhost:8080/token/"
customer_endpoint = "http://localhost:8080/customer/"
account_endpoint = "http://localhost:8080/accounts/"
merchant_endpoint = "http://localhost:8080/merchant/"
transaction_deposit_endpoint = "http://localhost:8080/deposit/"

customers_data = [
    {
        "name": "Customer - credit",
        "id_number": "3175023005910101",
        "email": "customercredit@gmail.com"
    },
    {
        "name": "Customer - ecommernce",
        "id_number": "3175023005910102",
        "email": "customerecommerce@gmail.com"
    },
    {
        "name": "Customer - education",
        "id_number": "3175023005910103",
        "email": "customereducation@gmail.com"
    },
    {
        "name": "Customer - electrical",
        "id_number": "3175023005910104",
        "email": "customerelectrical@gmail.com"
    },
    {
        "name": "Customer - emoney",
        "id_number": "3175023005910105",
        "email": "customeremoney@gmail.com"
    },
    {
        "name": "Customer - flight",
        "id_number": "3175023005910106",
        "email": "customerflight@gmail.com"
    },
    {
        "name": "Customer - insurance",
        "id_number": "3175023005910107",
        "email": "customerinsurance@gmail.com"
    },
    {
        "name": "Customer - internet quota",
        "id_number": "3175023005910107",
        "email": "customerinternetquota@gmail.com"
    },
    {
        "name": "Customer - multifinance",
        "id_number": "3175023005910108",
        "email": "customermultifinance@gmail.com"
    },
    {
        "name": "Customer - tax",
        "id_number": "3175023005910109",
        "email": "customertax@gmail.com"
    },
    {
        "name": "Customer - train",
        "id_number": "3175023005910110",
        "email": "customertrain@gmail.com"
    },
    {
        "name": "Customer - water",
        "id_number": "3175023005910111",
        "email": "customerwater@gmail.com"
    }
]

token = requests.post(token, data={'username': 'admin', 'password': 'password'}).json()
print(token['access_token'])

for data in customers_data:
    response = requests.post(customer_endpoint, json=data, headers={'Authorization': 'Bearer ' + token['access_token']})
    print(response.json())

for data in customers_data:
    data['account_type'] = "DEPOSIT"
    response = requests.post(account_endpoint, json=data, headers={'Authorization': 'Bearer ' + token['access_token']})
    print(response.json())

for data in customers_data:
    id_number = data['id_number']
    customer_response = requests.get(customer_endpoint + id_number, headers={'Authorization': 'Bearer ' + token['access_token']}).json()
    account_response = requests.get(account_endpoint + customer_response['cif_number'], headers={'Authorization': 'Bearer ' + token['access_token']}).json()
    account_number = account_response['data'][0]['account_number']
    transaction_response = requests.post(transaction_deposit_endpoint, json={ 'account_number' : account_number, 'amount' : 1000000 }, headers={'Authorization': 'Bearer YWRtaW4='})
    print(transaction_response.json())

for data in customers_data:
    id_number = data['id_number']
    customer_response = requests.get(customer_endpoint + id_number, headers={'Authorization': 'Bearer YWRtaW4='}).json()
    account_response = requests.get(account_endpoint + customer_response['cif_number'], headers={'Authorization': 'Bearer ' + token['access_token']}).json()
    data = {
        "name": customer_response['name'] + " merchant",
        "description": customer_response['name'] + " merchant",
        "cif_number": customer_response['cif_number'],
        "account_number": account_response['data'][0]['account_number']
    }
    merchant_response = requests.post(merchant_endpoint, json=data, headers={'Authorization': 'Bearer YWRtaW4='}).json()
    print(merchant_response)
