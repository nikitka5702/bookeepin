from django.contrib import admin

from main.models import Income, Expense, Category, Account


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'category_type')


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'account',
        'amount',
        'group',
        'date'
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'account',
        'amount',
        'cash_back',
        'group',
        'date'
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'user',
        'date_of_open',
        'date_of_close',
        'amount',
        'is_cash'
    )