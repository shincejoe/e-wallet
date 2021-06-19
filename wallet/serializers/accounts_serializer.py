"""
AUTHOR: SHINCE JOE SHAJI
DATE: 20-06-21
"""

"""
Serializer classes for formatting the data
"""

import pytz
from rest_framework import serializers
from e_wallet.settings import TIME_ZONE
from wallet.models import Account


class AccountInitializeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AccountsSerializer(serializers.ModelSerializer):
    status_choices = {1: 'enabled',
                      2: 'success',
                      3: 'disabled'}
    owned_by = serializers.SerializerMethodField(source='user')
    enabled_at = serializers.SerializerMethodField(source='updated_at')
    balance = serializers.FloatField(source='amount')

    def get_owned_by(self, obj):
        return str(obj.user.customer_id)

    def get_enabled_at(self, obj):
        return obj.updated_at.astimezone(pytz.timezone(TIME_ZONE))

    class Meta:
        model = Account
        fields = ['id', 'status', 'owned_by', 'enabled_at', 'balance']


class WalletFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class WalletWithdrawSerializer(serializers.ModelSerializer):
    status_choices = {1: 'enabled',
                      2: 'success',
                      3: 'disabled'}
    deposited_by = serializers.SerializerMethodField(source='user')
    deposited_at = serializers.SerializerMethodField(source='updated_at')
    status = serializers.SerializerMethodField()

    def get_deposited_by(self, obj):
        return str(obj.user.customer_id)

    def get_status(self, obj):
        return next(self.status_choices[item] for item in self.status_choices if item == obj.status)

    def get_deposited_at(self, obj):
        return obj.updated_at.astimezone(pytz.timezone(TIME_ZONE))

    class Meta:
        model = Account
        fields = ['id', 'status', 'deposited_by', 'deposited_at', 'amount', 'reference_id']


class WalletDepositSerializer(serializers.ModelSerializer):
    status_choices = {1: 'enabled',
                      2: 'success',
                      3: 'disabled'}
    deposited_by = serializers.SerializerMethodField(source='user')
    deposited_at = serializers.SerializerMethodField(source='updated_at')
    status = serializers.SerializerMethodField()

    def get_deposited_by(self, obj):
        return str(obj.user.customer_id)

    def get_status(self, obj):
        return next(self.status_choices[item] for item in self.status_choices if item == obj.status)

    def get_deposited_at(self, obj):
        return obj.updated_at.astimezone(pytz.timezone(TIME_ZONE))

    class Meta:
        model = Account
        fields = ['id', 'status', 'deposited_by', 'deposited_at', 'amount', 'reference_id']


class WalletDisableSerializer(serializers.ModelSerializer):
    status_choices = {1: 'enabled',
                      2: 'success',
                      3: 'disabled'}
    owned_by = serializers.SerializerMethodField(source='user')
    disabled_at = serializers.SerializerMethodField(source='updated_at')
    balance = serializers.FloatField(source='amount')

    def get_owned_by(self, obj):
        return str(obj.user.customer_id)

    def get_disabled_at(self, obj):
        return obj.updated_at.astimezone(pytz.timezone(TIME_ZONE))

    class Meta:
        model = Account
        fields = ['id', 'status', 'disabled_at', 'owned_by', 'balance']
