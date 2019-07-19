from django.contrib import admin

from main.models import Income, Expense, Category, Account

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Account)
