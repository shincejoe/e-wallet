"""
AUTHOR: SHINCE JOE SHAJI
DATE: 20-06-21
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from wallet.models import User, Account
from wallet.serializers.accounts_serializer import WalletDepositSerializer, WalletWithdrawSerializer

''' 
This API is used for creating a wallet account for a user 
'''


class WalletDepositView(APIView):
    serializer_class = WalletDepositSerializer

    def post(self, request, *args, **kwargs):
        data = {"data": {}, "status": "failed"}
        try:
            user_obj = request.auth.user
            accounts_obj = Account.objects.filter(user=user_obj).first()
            if accounts_obj and accounts_obj.status == 1:
                data = {"amount": float(request.data['amount']) + accounts_obj.amount, "reference_id": request.data['reference_id'], "user":user_obj.id}
                requested_data = self.serializer_class(data=data, instance=accounts_obj)
                if requested_data.is_valid():
                    requested_data.save()
                    wallet_data = {"deposit": requested_data.data}
                    data = {"data": wallet_data, "status": "success"}

        except Exception as ex:
            print(str(ex))

        return Response(data=data)


class WalletWithdrawalView(APIView):
    serializer_class = WalletWithdrawSerializer

    def post(self, request, *args, **kwargs):
        data = {"data": {}, "status": "failed"}
        try:
            user_obj = request.auth.user
            accounts_obj = Account.objects.filter(user=user_obj).first()
            if accounts_obj and accounts_obj.status == 1 and accounts_obj.amount >= float(request.data['amount']):
                data = {"amount": accounts_obj.amount - float(request.data['amount']),
                        "reference_id": request.data['reference_id'],
                        "user":user_obj.id}
                requested_data = self.serializer_class(data=data, instance=accounts_obj)
                if requested_data.is_valid():
                    requested_data.save()
                    wallet_data = {"deposit": requested_data.data}
                    data = {"data": wallet_data, "status": "success"}


        except Exception as ex:
            print(str(ex))

        return Response(data=data)
