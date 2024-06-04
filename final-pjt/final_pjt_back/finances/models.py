from django.db import models
from accounts.models import *

# 예금 상품
class DepositProduct(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    fin_prdt_nm = models.CharField(max_length=50)
    kor_co_nm = models.CharField(max_length=20)
    max_limit = models.PositiveIntegerField(null=True)
    join_way = models.CharField(max_length=50)
    join_deny = models.IntegerField()
    join_member = models.TextField()
    spcl_cnd = models.TextField()
    etc_note = models.TextField()

# 예금 상품 옵션
class DepositOption(models.Model):
    deposit = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    fin_co_no = models.CharField(max_length=20)
    # S: 단리, M: 복리
    intr_rate_type = models.CharField(max_length=2, null=True)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
    save_trm = models.CharField(max_length=3, null=True)

# 적금 상품
class SavingProduct(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    fin_prdt_nm = models.CharField(max_length=50)
    kor_co_nm = models.CharField(max_length=20)
    max_limit = models.PositiveIntegerField(null=True)
    join_way = models.CharField(max_length=50)
    join_deny = models.IntegerField()
    join_member = models.TextField()
    spcl_cnd = models.TextField()
    etc_note = models.TextField()

# 적금 상품 옵션
class SavingOption(models.Model):
    saving = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    fin_co_no = models.CharField(max_length=20)
    # S: 단리, M: 복리
    intr_rate_type = models.CharField(max_length=2, null=True)
    # S: 정액정립식, F: 자유적립식
    rsrv_type = models.CharField(max_length=2)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
    save_trm = models.CharField(max_length=3, null=True)

# 주식 정보
class StockProduct(models.Model):
    prdt_cd = models.CharField(max_length=10) # 종목 코드
    prdt_name = models.CharField(max_length=60) # 종목명
    end_price = models.IntegerField() # 조회일 종가
    fluctuation_rate = models.FloatField() # 등락률
    trade_amount = models.IntegerField() # 거래량
    trade_price_amount = models.IntegerField() # 거래대금
    capitalization = models.IntegerField() # 시가총액
    shared_amount = models.IntegerField() # 상장주식수
    idx_bztp_mcls_cd_name = models.CharField(max_length=60, blank=True) # 업종명
    one_before_end_price = models.IntegerField(blank=True, null=True)
    one_before_end_rate = models.FloatField(blank=True, null=True)
    two_before_end_price = models.IntegerField(blank=True, null=True)
    two_before_end_rate = models.FloatField(blank=True, null=True)
    three_before_end_price = models.IntegerField(blank=True, null=True)
    three_before_end_rate = models.FloatField(blank=True, null=True)


# 기업 정보
class CorporationDetail(models.Model):
    stock = models.ForeignKey(StockProduct, on_delete=models.CASCADE)
    crno = models.CharField(max_length=30) # 법인등록번호
    corpNm = models.CharField(max_length=300) # 법인명
    enpPbanCmpyNm = models.CharField(max_length=500) # 기업공시회사명
    enpDtadr = models.CharField(max_length=500) # 기업 상세주소
    enpHmpgUrl = models.CharField(max_length=300) # 홈페이지 URL
    enpTlno = models.CharField(max_length=100) # 전화번호
    enpEstbDt = models.CharField(max_length=8) # 기업설립일자
    enpEmpeCnt = models.IntegerField() # 기업종업원수
    enpPn1AvgSlryAmt = models.FloatField() # 기업1인평균급여금액
    enpMainBizNm = models.CharField(max_length=1000) # 기업주요사업명


# 예금 가입 정보
class DepositProductJoinInfo(models.Model):
    deposit_option = models.ForeignKey(DepositOption, on_delete=models.CASCADE)
    payment = models.PositiveIntegerField()
    is_prime_rate = models.BooleanField()
    join_date = models.DateField(auto_now_add=True)

# 적금 가입 정보
class SavingProductJoinInfo(models.Model):
    saving_option = models.ForeignKey(SavingOption, on_delete=models.CASCADE)
    monthly_payment = models.PositiveIntegerField()
    is_prime_rate = models.BooleanField()
    join_date = models.DateField(auto_now_add=True)

# 주식 구매 정보
class StockProductBuyInfo(models.Model):
    stock = models.ForeignKey(StockProduct, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    buy_date = models.DateField(auto_now_add=True)