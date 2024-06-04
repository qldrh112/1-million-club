from django.contrib.auth.hashers import make_password
import random
import requests
from datetime import datetime, timedelta
from finances.models import DepositProduct, SavingProduct, StockProduct, DepositOption, SavingOption

start = datetime.now() - timedelta(days=365)
end = datetime.now()

def banks():
    deposits = DepositProduct.objects.all()
    savings = SavingProduct.objects.all()

    # 주거래은행을 위한 은행 값 추출(중복 제거)
    deposit_kor_co_nm = list(deposits.values_list('kor_co_nm', flat=True))
    saving_kor_co_nm = list(savings.values_list('kor_co_nm', flat=True))
    
    return list(set(deposit_kor_co_nm + saving_kor_co_nm))


def industries():
    # 주식 정보에서 모든 업종 추출
    stocks = StockProduct.objects.all()
    return list(set(stocks.values_list('idx_bztp_mcls_cd_name', flat=True)))


def random_date(start, end):
    # 오늘부터 1년 전까지 날짜를 무작위로 반환하는 함수
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def make_data():
    # [참고] 현재 코드는 아래 User 모델을 기준으로 작성되어 있습니다.
    """
    class User(AbstractBaseUser):
        username = models.CharField(max_length=30, unique=True)
        nickname = models.CharField(max_length=255, blank=True, null=True)
        email = models.EmailField(max_length=254, blank=True, null=True)
        age = models.IntegerField(blank=True, null=True)
        money = models.IntegerField(blank=True, null=True)
        salary = models.IntegerField(blank=True, null=True)
        # 가입한 상품 목록 리스트를 ,로 구분된 문자열로 저장함
        financial_products = models.TextField(blank=True, null=True)

        # superuser fields
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
    """

    first_name_samples = '김이박최정강조윤장임송이배정김이최이이김이신이문한탁이김김박박안윤이조장조연신정박심장김나장박신'
    middle_name_samples = '민서예지도하주윤채현지창상원진호찬영소유민규희현재지호한보규성주홍채남승지창상기선태대시홍도지현우'
    last_name_samples = '준윤우원호후서연아은진용무빈영진규빈희안수석진복성웅준솔경림재연찬연경희현훈헌욱기수훈형성경호희형'


    def random_name():
        result = ''
        result += random.choice(first_name_samples)
        result += random.choice(middle_name_samples)
        result += random.choice(last_name_samples)
        return result + str(random.randint(1, 100))

    stocks = StockProduct.objects.all()

    kor_co_nm_list = banks()
    idx_bztp_mcls_cd_name_list = industries()
    

    deposit_length = DepositOption.objects.count()
    saving_length = SavingOption.objects.count()
    stock_length = stocks.count()

    # json 파일 만들기
    import json
    from collections import OrderedDict

    file = OrderedDict()

    username_list = []
    N = 10000
    i = 0

    while i < N:
        rn = random_name()
        if rn in username_list:
            continue

        username_list.append(rn)
        i += 1


    # 저장 위치는 프로젝트 구조에 맞게 수정합니다.
    user_data_save_dir = 'accounts/fixtures/accounts/user_data.json'
    with open(user_data_save_dir, 'w', encoding="utf-8") as f:
        f.write('[')
        for i in range(N):
            # 랜덤한 데이터를 삽입
            file['model'] = 'accounts.User'
            file['pk'] = i + 1
            file['fields'] = {
                'username': username_list[i],  # 유저 이름 랜덤 생성
                'password': 'pbkdf2_sha256$600000$oKx2nj31JpOlnxl04qMcu8$0qgdV+/yyrMvOOdy04P1AJSmduZlbEjZe2mdMzp3nf0=',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
            }
            json.dump(file, f, ensure_ascii=False, indent='\t')
            if i != N - 1:
                f.write(',')
        f.write(']')
        f.close()
    print(f'데이터 생성 완료 / 저장 위치: {user_data_save_dir}')

    # 포트폴리오 생성을 위한 데이터
    portfoliobase_data_save_dir = 'accounts/fixtures/accounts/portfolio_base_data.json'
    with open(portfoliobase_data_save_dir, 'w', encoding="utf-8") as f:
        f.write('[')
        for i in range(N):
            invest_aggresive = random.randrange(0, 100, 10)
            income_bracket = random.randint(1, 5)
            if income_bracket == 1:
                seed_money = random.randrange(1000000, 15000000, 1000000)
                salary = random.randrange(0, 800000, 10000)
            elif income_bracket == 2:
                seed_money = random.randrange(15000000, 24000000, 1000000)
                salary = random.randrange(800000, 1600000, 10000)
            elif income_bracket == 3:
                seed_money = random.randrange(24000000, 34000000, 1000000)
                salary = random.randrange(1600000, 1800000, 10000)
            elif income_bracket == 4:
                seed_money = random.randrange(34000000, 46000000, 1000000)
                salary = random.randrange(1800000, 2200000, 10000)
            elif income_bracket == 5:
                seed_money = random.randrange(46000000, 96000000, 1000000)
                salary = random.randrange(2200000, 3300000, 10000)
            target = round(random.uniform(seed_money, seed_money * 1.5))
            # 랜덤한 데이터를 삽입
            # 통계청 자료를 참고하여 1분위부터 5분위까지 평균 소득과 자산 활용
            file['model'] = 'accounts.portfoliobase'
            file['pk'] = i + 1
            file['fields'] = {
                'user': i + 1,
                'year': random.randint(1, 3),
                'income_bracket': income_bracket,
                'seed_money': seed_money,  # 현재 가진 금액
                'salary': salary,  # 월급
                'target': target, # 목표액
                'invest_aggresive': invest_aggresive,
                'invest_conservative': 100 - invest_aggresive,
                'age': random.randint(19, 80),  # 나이
                'kor_co_nm': random.choice(kor_co_nm_list),
                'is_prime_rate': random.choice([True, False]),
                'industry': random.choice(idx_bztp_mcls_cd_name_list),
            }

            json.dump(file, f, ensure_ascii=False, indent='\t')
            if i != N - 1:
                f.write(',')
        f.write(']')
        f.close()
    print(f'데이터 생성 완료 / 저장 위치: {portfoliobase_data_save_dir}')

    # 예금 가입 정보
    deposit_data_save_dir = 'accounts/fixtures/accounts/deposit_join_data.json'
    with open(deposit_data_save_dir, 'w', encoding="utf-8") as f:
        f.write('[')
        for i in range(N):
            # 랜덤한 데이터를 삽입
            file['model'] = 'finances.depositproductjoininfo'
            file['pk'] = i + 1
            file['fields'] = {
                'deposit_option': random.randint(1, deposit_length),
                'payment': random.randrange(1000000, 10000000, 1000000),
                'is_prime_rate': random.choice([True, False]),
                'join_date': random_date(start, end).strftime("%Y-%m-%d"),
            }
            json.dump(file, f, ensure_ascii=False, indent='\t')
            if i != N - 1:
                f.write(',')
        f.write(']')
        f.close()
    print(f'데이터 생성 완료 / 저장 위치: {deposit_data_save_dir}')


    # 적금 가입 정보
    saving_data_save_dir = 'accounts/fixtures/accounts/saving_join_data.json'
    with open(saving_data_save_dir, 'w', encoding="utf-8") as f:
        f.write('[')
        for i in range(N):
            # 랜덤한 데이터를 삽입
            file['model'] = 'finances.savingproductjoininfo'
            file['pk'] = i + 1
            file['fields'] = {
                'saving_option': random.randint(1, saving_length),
                'monthly_payment': random.randrange(100000, 1000000, 100000),
                'is_prime_rate': random.choice([True, False]),
                'join_date': random_date(start, end).strftime("%Y-%m-%d"),
            }
            json.dump(file, f, ensure_ascii=False, indent='\t')
            if i != N - 1:
                f.write(',')
        f.write(']')
        f.close()
    print(f'데이터 생성 완료 / 저장 위치: {saving_data_save_dir}')


    # 주식 구매 정보
    stock_data_save_dir = 'accounts/fixtures/accounts/stock_buy_data.json'
    with open(stock_data_save_dir, 'w', encoding="utf-8") as f:
        f.write('[')
        for i in range(N):
            # 랜덤한 데이터를 삽입
            file['model'] = 'finances.stockproductbuyinfo'
            file['pk'] = i + 1
            file['fields'] = {
                'stock': random.randint(1, stock_length),
                'amount': random.randint(1, 50),
                'buy_date': random_date(start, end).strftime("%Y-%m-%d"),
            }
            json.dump(file, f, ensure_ascii=False, indent='\t')
            if i != N - 1:
                f.write(',')
        f.write(']')
        f.close()
    print(f'데이터 생성 완료 / 저장 위치: {stock_data_save_dir}')


    # 포트폴리오 데이터
    portfolio_data_save_dir = 'accounts/fixtures/accounts/portfolio_data.json'
    with open(portfolio_data_save_dir, 'w', encoding="utf-8") as f:
        f.write('[')
        for i in range(N):
            # 랜덤한 데이터를 삽입
            file['model'] = 'accounts.portfolio'
            file['pk'] = i + 1
            file['fields'] = {
                'user': i + 1,
            # 랜덤한 0~2개의 상품을 가입하도록 삽입됨
                'deposit':
                    [
                        random.randint(1, deposit_length)
                        for _ in range(random.randint(0, 3))
                    ],
                'saving':
                    [
                        random.randint(1, saving_length)
                        for _ in range(random.randint(0, 3))
                    ],
                'stock':
                    [
                        random.randint(1, stock_length)
                        for _ in range(random.randint(0, 3))
                    ],
            }
            json.dump(file, f, ensure_ascii=False, indent='\t')
            if i != N - 1:
                f.write(',')
        f.write(']')
        f.close()
    print(f'데이터 생성 완료 / 저장 위치: {portfolio_data_save_dir}')
