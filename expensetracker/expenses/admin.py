from django.contrib import admin

from .models import Transaction, Currency, Category, Budget

admin.site.register(Transaction)
admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Budget)
