import coinaddr
from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
import asyncio
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import *
from django.views.decorators.csrf import csrf_exempt

from .models import BTCAddresses

###
# Etherscan API KEY
###
###
Etherscan_API = "HHSFMGXC1EFW7B3XJ4DX32R77XJS7K3JD1"


###
###
###


# Create your views here.
def user_balance(request, public_key):
    try:
        url = "https://blockchain.info/rawaddr/" + public_key

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        resp = response.json()

        return JsonResponse(resp, safe=False)
    except:
        url = "https://blockchain.info/rawaddr/" + public_key

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        return JsonResponse({"Error":response.text}, safe=False)

def BTC_balance2(request,public_key):
    url = "https://sochain.com/api/v2/address/BTC/" + public_key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    return JsonResponse(response, safe=False)

def BTC_latest_block(request):

    import requests

    url = "https://blockchain.info/latestblock"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    return JsonResponse(response, safe=False)


def BCH_address_detail(request, public_key):
    url = "https://rest.bitcoin.com/v2/address/details/bitcoincash:" + public_key
    x = 0
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    resp = response.json()
    url2 = "https://rest.bitcoin.com/v2/address/transactions/bitcoincash:" + public_key
    response2 = requests.request("GET", url2, headers=headers, data=payload)
    resp["transactions"] = response2.json()
    return JsonResponse(resp, safe=False)


def XLM_address_detail(request, public_key):


    url = "https://horizon.stellar.org/accounts/" + public_key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    resp = response.json()
    url_transctions = "https://horizon.stellar.org/accounts/GAIQSLA7ADQ3LTE4SSFPA5SSFJXV6FQH57B6KLE6HULKDGBDKSPNFVGZ/payments"

    response_transactions = requests.request("GET", url_transctions, headers=headers, data=payload)
    resp_transactions = response_transactions.json()

    resp = {"balances": resp["balances"],
            "transactions": resp_transactions["_embedded"]["records"]}
    return JsonResponse(resp, safe=False)


ERC20_token_contract_address = {
    "USDT": {"Token": "USDT", "contract_address": "0xdac17f958d2ee523a2206206994597c13d831ec7"},
    "LINK": {"Token": "LINK", "contract_address": "0x514910771af9ca656af840dff83e8264ecf986ca"},
    #"KNC": {"Token": "KNC", "contract_address": "0xdd974d5c2e2928dea5f71b9825b8b646686bd200"},
    #"XOR": {"Token": "XOR", "contract_address": "0x40FD72257597aA14C7231A7B1aaa29Fce868F677"},
    "BNB": {"Token": "BNB", "contract_address": "0xB8c77482e45F1F44dE1745F52C74426C631bDD52"},
    #"USDC": {"Token": "USDC", "contract_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"},
    #"WBTC": {"Token": "WBTC", "contract_address": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"},
    #"YFI": {"Token": "YFI", "contract_address": "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"},
    #"UNI": {"Token": "UNI", "contract_address": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"},
    "COMP": {"Token": "COMP", "contract_address": "0xc00e94cb662c3520282e6f5717214004a7f26888"},
    }


def util_ETH_token_balance(contract_dict, ETH_address):
    url = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + contract_dict[
        "contract_address"] + "&address=" + ETH_address + "&tag=latest&apikey=" + Etherscan_API

    payload = {}
    headers = {}

    resp = requests.request("GET", url, headers=headers, data=payload).json()
    return {contract_dict["Token"]: resp["result"]}


def ETH_address_detail_async(request, public_key):
    ####
    ####
    # ETH APIs is not standard in it's core so we should make it standard
    ###
    ###
    resp = {}
    url_list = []
    url_ETH_balance = "https://api.etherscan.io/api?module=account&action=balance&address=" + public_key + "&tag=latest&apikey=" + Etherscan_API
    url_token_transactions = "https://api.etherscan.io/api?module=account&action=tokentx&address=" + public_key + "&startblock=0&endblock=999999999&sort=asc&apikey=" + Etherscan_API
    url_transactions = "https://api.etherscan.io/api?module=account&action=txlist&address=" + public_key + "&startblock=0&endblock=99999999&sort=asc&apikey=" + Etherscan_API
    payload = {}
    headers = {}
    url_list.append(url_ETH_balance)
    url_list.append(url_token_transactions)
    url_list.append(url_transactions)
    for key, item in ERC20_token_contract_address.items():
        url_list.append("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" + item[
            "contract_address"] + "&address=" + public_key + "&tag=latest&apikey=" + Etherscan_API)
    # url_list=[]
    xxx = run_all_fetches(url_list)
    response_ETH_balance = xxx[0]
    response_ETH_token_transactions = xxx[1]
    response_ETH_transactions = xxx[2]
    token_balance_list = []
    for i, (key, item) in enumerate(ERC20_token_contract_address.items()):
        token_balance_list.append({key: xxx[i + 3]["result"]})

    resp = {"balances": {"ETH native balance": response_ETH_balance["result"],
                         "Token balances": token_balance_list,
                         },
            "NormalTransactions": list(reversed(response_ETH_transactions["result"])),
            "TokenTransactions": response_ETH_token_transactions["result"]
            }
    return JsonResponse(resp, safe=False)


def ETH_address_detail(request, public_key):
    ####
    ####
    # ETH APIs is not standard in it's core so we should make it standard
    ###
    ###
    resp = {}

    url_ETH_balance = "https://api.etherscan.io/api?module=account&action=balance&address=" + public_key + "&tag=latest&apikey=" + Etherscan_API
    url_token_transactions = "https://api.etherscan.io/api?module=account&action=tokentx&address=" + public_key + "&startblock=0&endblock=999999999&sort=asc&apikey=" + Etherscan_API
    url_transactions = "https://api.etherscan.io/api?module=account&action=txlist&address=" + public_key + "&startblock=0&endblock=99999999&sort=asc&apikey=" + Etherscan_API
    payload = {}
    headers = {}

    response_ETH_balance = requests.request("GET", url_ETH_balance, headers=headers, data=payload).json()
    response_ETH_token_transactions = requests.request("GET", url_token_transactions, headers=headers,
                                                       data=payload).json()
    response_ETH_transactions = requests.request("GET", url_transactions, headers=headers, data=payload).json()

    token_balances = {}
    for key, item in ERC20_token_contract_address.items():
        token_balances[key] = util_ETH_token_balance(item, public_key)[key]

    resp = {"balances": {"ETH native balance": response_ETH_balance["result"],
                         "Token balances": token_balances,
                         },
            "NormalTransactions": response_ETH_transactions["result"],
            "TokenTransactions": response_ETH_token_transactions["result"]
            }
    return JsonResponse(resp, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def give_address(request):
    addr = BTCAddresses.objects.filter(isUsed=False)[0]
    addr.isUsed = True
    addr.user_id = int(json.loads(request.body.decode("utf-8"))["userID"])
    addr.save()

    return JsonResponse({"address": addr.address, "Message": "We successfully submitted user with user ID of:  " + str(
        addr.user_id) + "  To our database"})

blocknative_API_key="f4c3d35d-b1e4-49b7-8e9f-76f0e82f52a1"



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_up_webhook(request):
    url = "https://api.blocknative.com/address"

    x = json.loads(request.body.decode("utf-8"))

    payload = "{\r\n    \"apiKey\": \""+ blocknative_API_key +"\",\r\n  " \
              "  \"address\": \""+ x["address"] +"\",\r\n  " \
              "  \"blockchain\": \""+ x["blockchain"] +"\",\r\n  " \
              "  \"networks\": [\r\n        \""+ x["network"] +"\"\r\n    ]\r\n}"
    headers = {
        'Content-Type': 'application/json'
    }


    ##We should also save



    resp = requests.request("POST", url, headers=headers, data=payload).json()


    return JsonResponse(resp)


# def DOGE_address_detail_async(request, public_key):
#     url = "https://sochain.com/api/v2/get_address_balance/DOGE/"+public_key
#     url_recieved_amount = "https://sochain.com/api/v2/get_address_received/DOGE/"+public_key
#     url_sent_amount = "https://sochain.com/api/v2/get_address_spent/DOGE/" + public_key
#     payload = {}
#     headers = {}
#
#     response = requests.request("GET", url, headers=headers, data=payload).json()
#     response_recieved_amount = requests.request("GET", url_recieved_amount, headers=headers, data=payload).json()["data"]["confirmed_received_value"]
#     response_sent_amount = requests.request("GET", url_sent_amount, headers=headers, data=payload).json()["data"]["confirmed_sent_value"]
#     response["data"]["confirmed_received_value"] =response_recieved_amount
#     response["data"]["confirmed_sent_value"] = response_sent_amount
#
#
#     response["tx"] =[get_DOGE_transaction_detail("6f47f0b2e1ec762698a9b62fa23b98881b03d052c9d8cb1d16bb0b04eb3b7c5b")]
#     return JsonResponse(response, safe=False)
#
#
# def get_DOGE_transaction_detail(tx_id):
#     url = "https://sochain.com/api/v2/tx/DOGE/" + tx_id
#
#     payload = {}
#     headers = {}
#
#     response = requests.request("GET", url, headers=headers, data=payload).json()["data"]
#     return response

#def get_DOGE_re



def DOGE_address_detail_async(request,public_key):
    url = "https://sochain.com/api/v2/address/DOGE/" + public_key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    return JsonResponse(response, safe=False)

def LTC_address_detail_async(request,public_key):
    url = "https://sochain.com/api/v2/address/LTC/" + public_key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    return JsonResponse(response, safe=False)
def DASH_address_detail_async(request,public_key):
    url = "https://sochain.com/api/v2/address/DASH/" + public_key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    return JsonResponse(response, safe=False)


def validate_BTC(request,public_key):
    try:
        validation=coinaddr.validate('btc', public_key)
        if validation.valid:
            return JsonResponse({"Address":public_key,"validation":validation.valid}, safe=False)
        else:
            return JsonResponse({"Address": public_key, "validation": validation.valid}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened" }, safe=False, status=500)


def validate_ETH(request,public_key):
    try:
        validation = coinaddr.validate('eth', public_key)
        if validation.valid:
            return JsonResponse({"Address":public_key , "validation":validation.valid}, safe=False)
        else:
            return JsonResponse({"Address": public_key, "validation": validation.valid}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened" }, safe=False, status=500)

def validate_LTC(request,public_key):
    try:
        validation = coinaddr.validate('ltc', public_key)
        if validation.valid:
            return JsonResponse({"Address":public_key , "validation":validation.valid}, safe=False)
        else:
            return JsonResponse({"Address": public_key, "validation": validation.valid}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened" }, safe=False, status=500)

def validate_DOGE(request,public_key):
    try:
        validation = coinaddr.validate('doge', public_key)
        if validation.valid:
            return JsonResponse({"Address":public_key , "validation":validation.valid}, safe=False)
        else:
            return JsonResponse({"Address": public_key, "validation": validation.valid}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened" }, safe=False, status=500)

def validate_XRP(request,public_key):
    try:
        validation = coinaddr.validate('xrp', public_key)
        if validation.valid:
            return JsonResponse({"Address":public_key , "validation":validation.valid}, safe=False)
        else:
            return JsonResponse({"Address": public_key, "validation": validation.valid}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened" }, safe=False, status=500)

def validate_DASH(request,public_key):
    try:
        validation = coinaddr.validate('dash', public_key)
        if validation.valid:
            return JsonResponse({"Address":public_key , "validation":validation.valid}, safe=False)
        else:
            return JsonResponse({"Address": public_key, "validation": validation.valid}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened" }, safe=False, status=500)

def validate_XLM(request,public_key):
    try:
        url = "https://horizon.stellar.org/accounts/"+ public_key

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return JsonResponse({"Address": public_key, "validation": True}, safe=False)
        else:
            response = response.json()
            return JsonResponse({"Address": public_key, "validation": False ,"response":response}, safe=False, status=417)
    except:
        return JsonResponse({"Error": "An unknown error happened"}, safe=False, status=500)
