from rest_framework import serializers
from .models import *
from finances.models import *
from finances.serializers import *

class PortfolioBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioBase
        fields = '__all__'
        read_only_fields = ('user', )

class CustomPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['deposits', 'savings', 'stock']

class DepositProductJoinInfoSerializer(serializers.ModelSerializer):
    options = DepositOptionProductSerializer(source='deposit_option', read_only=True)
    class Meta:
        model = DepositProductJoinInfo
        exclude = ('id', 'deposit_option',)

class SavingProductJoinInfoSerializer(serializers.ModelSerializer):
    options = SavingOptionProductSerializer(source='saving_option', read_only=True)
    class Meta:
        model = SavingProductJoinInfo
        exclude = ('id', 'saving_option',)

class StockProductBuyInfoSerializer(serializers.ModelSerializer):
    product = StockSerializer(source='stock', read_only=True)

    class Meta:
        model = StockProductBuyInfo
        exclude = ('id',)

#  데이터 정제
class M_PortfolioBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioBase
        exclude = ('id', 'year', 'target', )
        read_only_fields = ('user', )

class M_DepositProductJoinInfoSerializer(serializers.ModelSerializer):
    options = M_DepositOptionProductSerializer(source='deposit_option', read_only=True)
    class Meta:
        model = DepositProductJoinInfo
        exclude = ('id', 'deposit_option', 'payment', 'is_prime_rate', 'join_date', )

class M_SavingProductJoinInfoSerializer(serializers.ModelSerializer):
    options = M_SavingOptionProductSerializer(source='saving_option', read_only=True)
    class Meta:
        model = SavingProductJoinInfo
        exclude = ('id', 'saving_option', 'monthly_payment', 'is_prime_rate', 'join_date', )

class M_StockProductBuyInfoSerializer(serializers.ModelSerializer):
    product = M_StockSerializer(source='stock', read_only=True)

    class Meta:
        model = StockProductBuyInfo
        exclude = ('id', 'amount', 'buy_date', 'stock') 


    
    