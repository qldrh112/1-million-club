from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from finances.models import DepositProductJoinInfo, SavingProductJoinInfo, StockProductBuyInfo


class User(AbstractUser):
    pass


class PortfolioBase(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    target = models.PositiveIntegerField()
    seed_money = models.BigIntegerField()
    invest_aggresive = models.IntegerField()
    invest_conservative = models.IntegerField()
    salary = models.PositiveIntegerField()
    age = models.PositiveSmallIntegerField()
    kor_co_nm = models.CharField(max_length=30)
    industry = models.CharField(max_length=20)
    is_prime_rate = models.BooleanField()
    income_bracket = models.IntegerField(blank=True, null=True) # 소득분위



class Portfolio(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    deposit = models.ManyToManyField(DepositProductJoinInfo, related_name='deposit_comb')
    saving = models.ManyToManyField(SavingProductJoinInfo, related_name='saving_comb')
    stock = models.ManyToManyField(StockProductBuyInfo, related_name='stock_comb')
