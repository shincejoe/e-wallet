from django.contrib import admin

# Register your models here.
from wallet.models import Account, User, Transaction

admin.site.register(Account)
admin.site.register(User)
admin.site.register(Transaction)
