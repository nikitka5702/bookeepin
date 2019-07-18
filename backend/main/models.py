from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    class Meta:
        db_table = 'group'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)


class BaseRecord(models.Model):
    class Meta:
        abstract = True

    description = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    group = models.ForeignKey(Group, models.CASCADE)


class Account(models.Model):
    class Meta:
        db_table = 'account'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_open = models.DateField()
    date_of_close = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length=255)


class Income(BaseRecord):
    class Meta:
        db_table = 'income'


class Cost(BaseRecord):
    class Meta:
        db_table = 'cost'

    cash_back = models.FloatField(default=0.0)
