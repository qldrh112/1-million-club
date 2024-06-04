from rest_framework import serializers
from .models import *
from accounts.models import PortfolioBase, Portfolio

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit', )


class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'
    depositoption_set = DepositOptionSerializer(many=True, read_only=True)
    

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving', )

class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'
    savingoption_set = SavingOptionSerializer(many=True, read_only=True)

class FinanceCorportaionNameSerializer(serializers.Serializer):
    kor_co_nm = serializers.CharField()

    def get_names(self, instance):
        """
        예금, 적금 모델에서 금융사 이름을 가져와 중복을 제거하는 함수 
        """
        deposit_kor_co_nm = DepositProduct.objects.values_list('kor_co_nm', flat=True)
        saving_kor_co_nm = SavingProduct.objects.values_list('kor_co_nm', flat=True)
        
        kor_co_nms = set(deposit_kor_co_nm) | set(saving_kor_co_nm)

        return {'kor_co_nm': list(kor_co_nms)}

class DepositProductNotOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'

class DepositOptionProductSerializer(serializers.ModelSerializer):
    product = DepositProductNotOptionSerializer(source='deposit')

    class Meta:
        model = DepositOption
        exclude = ('id', 'deposit',)
        read_only_fields = ('deposit', )

class SavingProductNotOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = '__all__'

class SavingOptionProductSerializer(serializers.ModelSerializer):
    product = SavingProductNotOptionSerializer(source='saving')

    class Meta:
        model = SavingOption
        exclude = ('id', 'saving',)
        read_only_fields = ('saving',)

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = '__all__'

# 데이터 정제

class M_DepositProductNotOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = ('fin_prdt_nm', )


class M_DepositOptionProductSerializer(serializers.ModelSerializer):
    product = M_DepositProductNotOptionSerializer(source='deposit')

    class Meta:
        model = DepositOption
        exclude = ('id', 'deposit', 'fin_co_no', 'intr_rate_type', )
        read_only_fields = ('deposit', )

class M_SavingProductNotOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = ('fin_prdt_nm', )

class M_SavingOptionProductSerializer(serializers.ModelSerializer):
    product = M_SavingProductNotOptionSerializer(source='saving')

    class Meta:
        model = SavingOption
        exclude = ('id', 'saving', 'fin_co_no', 'intr_rate_type', 'rsrv_type', )
        read_only_fields = ('saving',)

class M_StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ('prdt_name', 'idx_bztp_mcls_cd_name', )