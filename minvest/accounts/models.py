from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from portfolio.models import Portfolio


class CustomUser(AbstractUser):
    customer_id = models.TextField(max_length=30, blank=True, default='')
    account_id = models.TextField(max_length=30, blank=True, default='')
    book_value = models.FloatField()
    portfolio = models.ForeignKey(Portfolio)
    investment_value = models.FloatField()
    share_amount = models.IntegerField()

    def update_investment_value(self):
        self.investment_value = self.portfolio.share_price * self.share_amount
        self.save()

    def deposit(self, value):
        self.update_investment_value()
        shares_bought = value / self.portfolio.share_price
        self.book_value += value
        self.investment_value += value
        self.share_amount += shares_bought
        self.save()

    def withdraw(self, value):
        self.update_investment_value()
        shares_sold = value / self.portfolio.share_price
        if shares_sold < self.share_amount:
            self.book_value = (self.investment_value - value) / (self.investment_value) * self.book_value
            self.investment_value -= value
            self.share_amount -= shares_sold
            self.save()