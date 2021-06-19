"""
AUTHOR: SHINCE JOE SHAJI
DATE: 20-06-21
"""

from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.manage_wallet import WalletDepositView, WalletWithdrawalView
from .views.wallet_initializer import WalletInitializer, EnableWalletView

router = DefaultRouter()
urlpatterns = [
    url('init', WalletInitializer.as_view(), name='init'),
    url('wallet', EnableWalletView.as_view(), name='wallet'),
    url('add-money', WalletDepositView.as_view(), name='add-money'),
    url('withdraw-money', WalletWithdrawalView.as_view(), name='withdraw-money'),
    path('', include(router.urls)),
]