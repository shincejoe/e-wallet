"""
AUTHOR: SHINCE JOE SHAJI
DATE: 20-06-21
"""


from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from wallet.models import User, Account
from wallet.serializers.accounts_serializer import AccountsSerializer, AccountInitializeSerializer, WalletDisableSerializer

''' 
These API's creates a wallet account for a user, enables the wallet, fetches necessary information of wallet 
'''

status_choices = {1: 'enabled',
                  2: 'success',
                  3: 'disabled'}


class WalletInitializer(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountInitializeSerializer

    def post(self, request, *args, **kwargs):
        status = "failed"
        data = {}
        try:
            if request.data and request.data['customer_xid']:
                user_profile = User.objects.filter(customer_id=request.data['customer_xid']).first()
                user_data = {
                    "user": user_profile.id,
                }
                serialized_data = self.serializer_class(data=user_data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    status = "success"
                    data = {
                        "data": {"token": Token.objects.filter(user=user_profile.id).first().pk},
                        "status": status

                    }
                else:
                    data = {"data": data, "success": status}
            else:
                data = {data: {}, status: "failed"}
        except Exception as ex:
            print(str(ex))
            data = {}
        return Response(data=data)


class EnableWalletView(APIView):
    serializer_class = AccountsSerializer

    def post(self, request):
        data = {"data": {}, "status": "failed"}

        try:
            user_obj = request.auth.user
            accounts_obj = Account.objects.filter(user=user_obj).first()
            if accounts_obj and accounts_obj.status != 1:
                data = {"status": 1}
                requested_data = self.serializer_class(data=data, instance=accounts_obj, partial=True)
                if requested_data.is_valid():
                    requested_data.save()
                    requested_data = dict(requested_data.data)
                    requested_data['status'] = next(status_choices[item] for item in status_choices if item == 1)
                    wallet_data = {
                        "wallet": requested_data
                    }
                    data = {"data": wallet_data, "status": "success"}

        except Exception as ex:
            print(str(ex))

        return Response(data=data)

    def get(self, request):
        data = {"data": {}, "status": "failed"}
        try:
            user_obj = request.auth.user
            accounts_obj = Account.objects.filter(user=user_obj).first()
            if accounts_obj:
                wallet_data = {"wallet": {
                            "id": accounts_obj.id,
                            "owned_by": user_obj.customer_id,
                            "status": next(status_choices[item] for item in status_choices
                                           if item == accounts_obj.status),
                            "enabled_at": accounts_obj.updated_at,
                            "balance": accounts_obj.amount}}
                data = {"data": wallet_data, "status": "success"}

        except Exception as ex:
            print(str(ex))

        return Response(data=data)

    def patch(self, request):
        data = {"data": {}, "status": "failed"}
        try:
            user_obj = request.auth.user
            accounts_obj = Account.objects.filter(user=user_obj).first()
            if accounts_obj:
                data = {"status": 3}
                requested_data = WalletDisableSerializer(data=data, instance=accounts_obj, partial=True)
                if requested_data.is_valid():
                    requested_data.save()
                    requested_data = requested_data.data
                    requested_data['status'] = next(status_choices[item] for item in status_choices if item == 3)
                    wallet_data = {"wallet": requested_data}
                    data = {"data": wallet_data, "status": "success"}

        except Exception as ex:
            print(str(ex))

        return Response(data=data)
