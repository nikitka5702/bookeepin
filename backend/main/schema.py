import datetime

import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Income, Expense, Category, Account

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username', 'email')


class IncomeType(DjangoObjectType):
    class Meta:
        model = Income


class ExpenseType(DjangoObjectType):
    class Meta:
        model = Expense


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        only_fields = ('id', 'name', 'category_type', 'user')


class AccountType(DjangoObjectType):
    class Meta:
        model = Account


# Create Mutations
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
        try:
            user.save()
        except IntegrityError:
            raise GraphQLError('User with given credentials already exists')

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
        account = Account.objects.filter(id=account).first()
        if group:
            group = Category.objects.filter(id=group).first()
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
        account = Account.objects.filter(id=account).first()
        if group:
            group = Category.objects.filter(id=group).first()
        if not cash_back:
            cash_back = 0.0
        if not date:
            date = datetime.date.today()

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
        category_type = graphene.String()
        description = graphene.String()

    def mutate(self, info, category_type, description):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        category = Category.objects.create(
            user=user,
            category_type=category_type,
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


# Update Mutations
class IncomeInput(graphene.InputObjectType):
    description = graphene.String(required=False)
    amount = graphene.Float(required=False)
    date = graphene.Date(required=False)
    group = graphene.Int(required=False)


class UpdateIncome(graphene.Mutation):
    income = graphene.Field(IncomeType)

    class Arguments:
        id = graphene.Int()
        income_data = IncomeInput()

    def mutate(self, info, id, income_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        income = Income.objects.filter(id=id).first()

        for attr, value in income_data.items():
            setattr(income, attr, value)

        try:
            income.full_clean()
            income.save()
            return UpdateIncome(income=income)
        except ValidationError as e:
            return UpdateIncome(income=income, errors=e)


class ExpenseInput(graphene.InputObjectType):
    description = graphene.String(required=False)
    amount = graphene.Float(required=False)
    date = graphene.Date(required=False)
    group = graphene.Int(required=False)
    cash_back = graphene.Float(required=False)


class UpdateExpense(graphene.Mutation):
    expense = graphene.Field(ExpenseType)

    class Arguments:
        id = graphene.Int()
        expense_data = IncomeInput()

    def mutate(self, info, id, expense_data):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        expense = Expense.objects.filter(id=id).first()

        for attr, value in expense_data.items():
            setattr(expense, attr, value)

        try:
            expense.full_clean()
            expense.save()
            return UpdateExpense(expense=expense)
        except ValidationError as e:
            return UpdateExpense(expense=expense, errors=e)


class CategoryInput(graphene.InputObjectType):
    category_type = graphene.String(reqired=False)
    description = graphene.String(required=False)


class UpdateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        id = graphene.Int()
        category_data = CategoryInput()

    def mutate(self, info, category_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        category = Category.objects.filter(id=id).first()

        for attr, value in category_data.items():
            setattr(category, attr, value)

        try:
            category.full_clean()
            category.save()
            return UpdateCategory(category=category)
        except ValidationError as e:
            return UpdateCategory(category=category, errors=e)


class AccountIncome(graphene.InputObjectType):
    amount = graphene.Float(required=False)
    description = graphene.String(required=False)
    is_cash = graphene.Boolean(required=False)
    date_of_open = graphene.Date(required=False)
    date_of_close = graphene.Date(required=False)


class UpdateAccount(graphene.Mutation):
    account = graphene.Field(CategoryType)

    class Arguments:
        id = graphene.Int()
        account_data = AccountIncome()

    def mutate(self, info, id, account_data):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        account = Account.objects.filter(id=id).first()

        for attr, value in account_data.items():
            setattr(account, attr, value)

        try:
            account.full_clean()
            account.save()
            return UpdateAccount(account=account)
        except ValidationError as e:
            return UpdateAccount(account=account, errors=e)


# Delete Mutations
class DeleteMutation(graphene.Mutation):
    result = graphene.String()
    model: models.Model

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in!')
        item = self.model.objects.get(id=id)
        if item.creator != user:
            raise GraphQLError('Wrong user!')
        else:
            item.delete()
            return self.__class__(result="Done")


class DeleteIncome(DeleteMutation):
    model = Income


class DeleteExpense(DeleteMutation):
    model = Expense


class DeleteCategory(DeleteMutation):
    model = Category


class DeleteAccount(DeleteMutation):
    model = Account


def _get_qs(model, search=None, first=None, skip=None):
    qs = model.objects.all()
    total = qs.count()
    if search:
        qs = qs.filter(search)
    if skip:
        qs = qs[skip:]
    if first:
        qs = qs[:first]
    return qs, total


class IncomeQueryType(graphene.ObjectType):
    incomes = graphene.List(IncomeType)
    total = graphene.Int()


class ExpenseQueryType(graphene.ObjectType):
    expenses = graphene.List(ExpenseType)
    total = graphene.Int()


class AccountQueryType(graphene.ObjectType):
    accounts = graphene.List(AccountType)
    total = graphene.Int()


class CategoryQueryType(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    total = graphene.Int()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    total_incomes = graphene.Field(
        IncomeQueryType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )
    total_expenses = graphene.Field(
        ExpenseQueryType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )
    total_accounts = graphene.Field(
        AccountQueryType
    )
    total_categories = graphene.Field(
        CategoryQueryType,
        category_type=graphene.NonNull(graphene.String),
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Not logged in!')
        return user

    def resolve_total_incomes(self, info, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        if search:
            search = Q(description=search) & Q(account__user=user)
        else:
            search = Q(account__user=user)

        return IncomeQueryType(*_get_qs(Income, search, first, skip))

    def resolve_total_expenses(self, info, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        if search:
            search = Q(description=search) & Q(account__user=user)
        else:
            search = Q(account__user=user)

        return ExpenseQueryType(*_get_qs(Expense, search, first, skip))

    def resolve_total_accounts(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')
        qs = Account.objects.filter(user=user).all()
        total = qs.count()

        return AccountQueryType(qs, total)

    def resolve_total_categories(self, info, category_type, search=None, first=None, skip=None, **kwargs):
        user = info.context.user
        if user.is_anonymous or not user.is_active:
            raise GraphQLError('You must be logged in!')

        if search:
            search = Q(category_type=category_type) & Q(description=search) & Q(user=user)
        else:
            search = Q(category_type=category_type) & Q(user=user)

        return CategoryQueryType(*_get_qs(Category, search, first, skip))


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_income = CreateIncome.Field()
    create_expense = CreateExpense.Field()
    create_category = CreateCategory.Field()
    create_account = CreateAccount.Field()

    update_income = UpdateIncome.Field()
    update_expense = UpdateExpense.Field()
    update_category = UpdateCategory.Field()
    update_account = UpdateAccount.Field()

    delete_income = DeleteIncome.Field()
    delete_expense = DeleteExpense.Field()
    delete_category = DeleteCategory.Field()
    delete_account = DeleteAccount.Field()
