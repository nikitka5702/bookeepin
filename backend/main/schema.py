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

        return Account.objects.filter(user=user)

    def resolve_categories(self, info):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        return Category.objects.filter(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
