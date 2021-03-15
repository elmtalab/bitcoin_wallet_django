"""bitcoin_wallet_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from commonAPI.views import user_balance, give_address, BCH_address_detail, XLM_address_detail, ETH_address_detail, \
    ETH_address_detail_async, set_up_webhook, DOGE_address_detail_async, LTC_address_detail_async, \
    DASH_address_detail_async, BTC_latest_block, BTC_balance2, validate_BTC, validate_ETH, validate_DOGE, validate_XLM, \
    validate_LTC, validate_DASH, validate_XRP
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/balance/BTC/<slug:public_key>', user_balance, name="BTC_address_detail"),
    path('user/balance/BTC2/<slug:public_key>', BTC_balance2, name="BTC_address_detail2"),
    path('BTC/latestblock', BTC_latest_block, name="BTC_latestblock"),
    path('user/balance/BCH/<slug:public_key>', BCH_address_detail, name="BCH_address_detail"),
    path('user/balance/XLM/<slug:public_key>', XLM_address_detail, name="XLM_address_detail"),
    #out-dated
    #path('user/balance/ETH/<slug:public_key>', ETH_address_detail, name="ETH_address_detail"),
    path('user/balance/ETH/<slug:public_key>', ETH_address_detail_async, name="ETH_address_detail"),
    path('user/balance/DOGE/<slug:public_key>', DOGE_address_detail_async, name="DOGE_address_detail"),
    path('user/balance/LTC/<slug:public_key>', LTC_address_detail_async, name="LTC_address_detail"),
    path('user/balance/DASH/<slug:public_key>', DASH_address_detail_async, name="DASH_address_detail"),

    #validate Crypto
    path('validate/BTC/<slug:public_key>', validate_BTC, name="validate_BTC"),
    #path('validate/BCH/<slug:public_key>', validate_BCH, name="BCH_address_detail"),
    path('validate/XLM/<slug:public_key>', validate_XLM, name="validate_XLM"),
    path('validate/XRP/<slug:public_key>', validate_XRP, name="validate_XRP"),
    path('validate/ETH/<slug:public_key>', validate_ETH, name="validate_ETH"),
    path('validate/DOGE/<slug:public_key>', validate_DOGE, name="validate_DOGE"),
    path('validate/LTC/<slug:public_key>', validate_LTC, name="validate_LTC"),
    path('validate/DASH/<slug:public_key>', validate_DASH, name="validate_DASH"),
    #Webhook and addresses
    path('user/giveAddress/', give_address, name="giveAddress"),
    path('user/setUpWebhook/', set_up_webhook, name="set_up_webhook"),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
