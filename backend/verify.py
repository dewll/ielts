import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization":os.environ['PAYSTACK_AUTHORIZATION_KEY']}
    response = requests. get(url, headers=headers)
    Json_Response = response.json()
    print(Json_Response)
    return Json_Response['data']['status']