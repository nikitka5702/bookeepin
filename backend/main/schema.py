import re

import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from backend.main.models import Income, Expense, Category, Account


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username')


class IncomeType(DjangoObjectType):
    class Meta:
        model = Income


class ExpenseType(DjangoObjectType):
    class Meta:
        model = Expense


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class AccountType(DjangoObjectType):
    class Meta:
        model = Account


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class CreateIncome(graphene.Mutation):
    income = graphene.Field(IncomeType)

    class Arguments:
        account = graphene.Int()
        description = graphene.String()
        amount = graphene.Float()
        date = graphene.Date()
        group = graphene.Int()

    def mutate(self, info, account, description, amount, date=None, group=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        income = Income.objects.create(
            account=account,
            description=description,
            amount=amount,
            date=date,
            group=group,
        )

        return CreateIncome(income=income)


class CreateExpense(graphene.Mutation):
    expense = graphene.Field(ExpenseType)

    class Arguments:
        account = graphene.Int()
        description = graphene.String()
        amount = graphene.Float()
        date = graphene.Date()
        group = graphene.Int()
        cash_back = graphene.Float()

    def mutate(self, info, account, description, amount, date=None, group=None, cash_back=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        expense = Expense.objects.create(
            account=account,
            description=description,
            amount=amount,
            date=date,
            group=group,
            cash_back=cash_back,
        )

        return CreateExpense(expense=expense)


class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        description = graphene.String()

    def mutate(self, info, description):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        category = Income.objects.create(
            user=user,
            description=description,
        )

        return CreateCategory(category=category)


class CreateAccount(graphene.Mutation):
    account = graphene.Field(CategoryType)

    class Arguments:
        amount = graphene.Float()
        description = graphene.String()
        is_cash = graphene.Boolean()
        date_of_open = graphene.Date()
        date_of_close = graphene.Date()

    def mutate(self, info, amount, description, is_cash, date_of_open=None, date_of_close=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        account = Account.objects.create(
            date_of_open=date_of_open,
            date_of_close=date_of_close,
            amount=amount,
            description=description,
            is_cash=is_cash,
        )

        return CreateAccount(account=account)


class Query(graphene.ObjectType):
    incomes = graphene.List(IncomeType)
    expenses = graphene.List(ExpenseType)

    accounts = graphene.List(AccountType)
    categories = graphene.List(CategoryType)

    def resolve_incomes(self, info):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        return Income.objects.filter(account__user=user)

    def resolve_expenses(self, info):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        return Expense.objects.filter(account__user=user)

    def resolve_accounts(self, info):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        return Account.objects.filter(user=user).values('id', 'description')

    def resolve_categories(self, info):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        return Category.objects.filter(user=user).values('id', 'description')


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
