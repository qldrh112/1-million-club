from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

from accounts import make_data, make_data2
from accounts.models import *
from accounts.serializers import *
from finances.serializers import *

import FinanceDataReader as fdr
from bs4 import BeautifulSoup
from io import BytesIO
from pandas import json_normalize
import pandas as pd
import requests
import time
import json
import re

import io
import base64
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


base_dir = settings.BASE_DIR
DATA_GOV_API_KEY = settings.DATA_GOV_API_KEY
FINLIFE_API_KEY=settings.FINLIFE_API_KEY
KOREA_INVEST_API_KEY=settings.KOREA_INVEST_API_KEY
KOREA_INVEST_SECRET=settings.KOREA_INVEST_SECRET
EXCHANGE_RATE_API_KEY=settings.EXCHANGE_RATE_API_KEY


# 금융상품한눈에
FINLIFE_BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
DEPOSIT_SEARCH_URL = FINLIFE_BASE_URL + 'depositProductsSearch.json'
SAVING_SEARCH_URL = FINLIFE_BASE_URL + 'savingProductsSearch.json'

finlife_params = {
    'auth': FINLIFE_API_KEY,
    'topFinGrpNo': '020000',
    'pageNo': 1,
}

# 공공데이터 포털
DATA_GOV_BASE_URL = 'https://apis.data.go.kr/1160100/service/'
CORP_SEARCH_URL = DATA_GOV_BASE_URL + 'GetFinaStatInfoService_V2/getSummFinaStat_V2'
data_gov_params = {
    'serviceKey': DATA_GOV_API_KEY,
    'numOfRows': 1,
    'pageNo': 1,
    'resultType': 'json',
    # 법인등록번호
    'crno': '1746110000741',
}

# 한국투자증권 API
access_token = ''
appkey=KOREA_INVEST_API_KEY
appsecret=KOREA_INVEST_SECRET

# API(모의계좌)
base_url = 'https://openapi.koreainvestment.com:9443'

# 기업정보
COPSERATION_URL = DATA_GOV_BASE_URL + 'GetCorpBasicInfoService_V2/getCorpOutline_V2'
coperation_params = {
    'serviceKey': KOREA_INVEST_API_KEY,
    'numOfRows': 1,
    'pageNo': 1,
    'resultType': 'json',
}

def stock_products_search(request):
    path = '/uapi/domestic-stock/v1/quotations/inquire-price'
    url = base_url + path

    headers = {
        'content-type':'application/json',
        'authorization':f'Bearer {access_token}',
        'appkey':appkey,
        'appsecret':appsecret,
        'tr_id':'FHKST01010100',
    }

    params = {
        'FID_COND_MRKT_DIV_CODE':'J', 
        'FID_INPUT_ISCD':'005930'
    }

    res = requests.post(url, headers=headers, params=params)
    data = res.json()['output']
    response = request.get()


def main(request):
    pass

def create_data(request):
    # 데이터 요청
    deposit_res = requests.get(DEPOSIT_SEARCH_URL, params=finlife_params).json()
    saving_res = requests.get(SAVING_SEARCH_URL, params=finlife_params).json()

    # 데이터 추출
    deposits = deposit_res.get('result').get('baseList')
    deposit_options = deposit_res.get('result').get('optionList')
    savings = saving_res.get('result').get('baseList')
    saving_options = saving_res.get('result').get('optionList')

    # DB에 추가 - 예금 상품
    for deposit in deposits:
        if DepositProduct.objects.filter(fin_prdt_cd=deposit.get('fin_prdt_cd')):
            continue
        else:
            data = {
            'fin_prdt_cd': deposit.get('fin_prdt_cd'),
            'fin_prdt_nm': deposit.get('fin_prdt_nm'),
            'kor_co_nm': deposit.get('kor_co_nm'),
            'max_limit': deposit.get('max_limit'),
            'join_way': deposit.get('join_way'),
            'join_deny': deposit.get('join_deny'),
            'join_member': deposit.get('join_member'),
            'spcl_cnd': deposit.get('spcl_cnd'),
            'etc_note': deposit.get('etc_note'),
        }
            deposit_serializer = DepositProductSerializer(data=data)
            if deposit_serializer.is_valid(raise_exception=True):
                deposit_serializer.save()

    # DB에 추가 - 예금 옵션
    for option in deposit_options:
        data = {
            'fin_co_no': option.get('fin_co_no'),
            'intr_rate_type': option.get('intr_rate_type'),
            'intr_rate': option.get('intr_rate'),
            'intr_rate2': option.get('intr_rate2'),
            'save_trm': option.get('save_trm'),
        }
        option_serializer = DepositOptionSerializer(data=data)
        if option_serializer.is_valid(raise_exception=True):
            deposit = get_object_or_404(DepositProduct, fin_prdt_cd=option.get('fin_prdt_cd'))
            option_serializer.save(deposit=deposit)

    # DB에 추가 - 적금 상품
    for saving in savings:
        if SavingProduct.objects.filter(fin_prdt_cd=saving.get('fin_prdt_cd')):
            continue
        else:
            data = {
            'fin_prdt_cd': saving.get('fin_prdt_cd'),
            'fin_prdt_nm': saving.get('fin_prdt_nm'),
            'kor_co_nm': saving.get('kor_co_nm'),
            'max_limit': saving.get('max_limit'),
            'join_way': saving.get('join_way'),
            'join_deny': saving.get('join_deny'),
            'join_member': saving.get('join_member'),
            'spcl_cnd': saving.get('spcl_cnd'),
            'etc_note': saving.get('etc_note'),
        }
            saving_serializer = SavingProductSerializer(data=data)
            if saving_serializer.is_valid(raise_exception=True):
                saving_serializer.save()

    # DB에 추가 - 적금 옵션
    for option in saving_options:
        data = {
            'fin_co_no': option.get('fin_co_no'),
            'intr_rate_type': option.get('intr_rate_type'),
            'rsrv_type': option.get('rsrv_type'),
            'intr_rate': option.get('intr_rate'),
            'intr_rate2': option.get('intr_rate2'),
            'save_trm': option.get('save_trm'),
        }
        option_serializer = SavingOptionSerializer(data=data)
        if option_serializer.is_valid(raise_exception=True):
            saving = SavingProduct.objects.get(fin_prdt_cd=option.get('fin_prdt_cd'))
            option_serializer.save(saving=saving)
    
    # 주식 정보 추가
    # 마지막 장 마감일 parsing
    url = 'https://finance.naver.com/sise/sise_index.naver?code=KOSPI'
    data = requests.get(url)
    data_html = BeautifulSoup(data.content)
    parse_day = data_html.select_one('div.ly_realtime > span#time').text.split()[0]
    biz_day = re.findall('[0-9]+', parse_day)
    biz_day = ''.join(biz_day)

    # hour = time.localtime()[3]
    # if hour < 9:
    #     biz_day = str(int(biz_day) - 1)
    #     hour = time.localtime()[3]


    # 주식 정보
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd' # base_url
    down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd' # download_url
    headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'} # headers
    
    # 전종목시세 csv 다운로드
    gen_otp_stk = {
        'mktId': 'STK',
        'trdDd': biz_day,
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01501'
    }
    otp_stk = requests.post(gen_otp_url, gen_otp_stk, headers=headers).text # otp 발급

    down_sector_stk = requests.post(down_url, {'code': otp_stk}, headers=headers) # csv_download
    sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR')

    # 1년 전 주식 데이터
    startdate_1 = pd.to_datetime(biz_day)
    startdate_1 = startdate_1 - pd.Timedelta(days=365)

    while startdate_1.weekday() >= 5:
        startdate_1 = startdate_1 - pd.Timedelta(days=1)
    startdate_1 = startdate_1.strftime('%Y%m%d')

    gen_otp_stk = {
        'mktId': 'STK',
        'strtDd':12,
        'strtDd' : startdate_1,
        'endDd': biz_day,
        'adjStkPrc_check':'Y',
        'adjStkPrc':'2',
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01602'
    }
    otp_stk = requests.post(gen_otp_url, gen_otp_stk, headers=headers).text

    down_sector_stk = requests.post(down_url, {'code': otp_stk}, headers=headers)
    before_stock_1 = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR')

    # 2년 전 주식 데이터
    startdate_2 = pd.to_datetime(biz_day)
    startdate_2 = startdate_2 - pd.Timedelta(days=365 * 2)

    while startdate_2.weekday() >= 5:
        startdate_2 = startdate_2 - pd.Timedelta(days=1)
    startdate_2 = startdate_2.strftime('%Y%m%d')

    gen_otp_stk = {
        'mktId': 'STK',
        'strtDd':12,
        'strtDd' : startdate_2,
        'endDd': biz_day,
        'adjStkPrc_check':'Y',
        'adjStkPrc':'2',
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01602'
    }
    otp_stk = requests.post(gen_otp_url, gen_otp_stk, headers=headers).text

    down_sector_stk = requests.post(down_url, {'code': otp_stk}, headers=headers)
    before_stock_2 = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR')

    # 3년 전 주식 데이터
    startdate_3 = pd.to_datetime(biz_day)
    startdate_3 = startdate_3 - pd.Timedelta(days=365 * 3)

    while startdate_3.weekday() >= 5:
        startdate_3 = startdate_3 - pd.Timedelta(days=1)
    startdate_3 = startdate_3.strftime('%Y%m%d')

    gen_otp_stk = {
        'mktId': 'STK',
        'strtDd':12,
        'strtDd' : startdate_3,
        'endDd': biz_day,
        'adjStkPrc_check':'Y',
        'adjStkPrc':'2',
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01602'
    }
    otp_stk = requests.post(gen_otp_url, gen_otp_stk, headers=headers).text

    down_sector_stk = requests.post(down_url, {'code': otp_stk}, headers=headers)
    before_stock_3 = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR')

    # 업종정보 csv 다운로드
    gen_otp_stk = {
        'mktId': 'STK',
        'trdDd': biz_day,
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
    }
    otp_stk = requests.post(gen_otp_url, gen_otp_stk, headers=headers).text # otp 발급

    down_business_stk = requests.post(down_url, {'code': otp_stk}, headers=headers) # csv_download
    business_stk = pd.read_csv(BytesIO(down_business_stk.content), encoding='EUC-KR')

    stock_1 = list(before_stock_1['종목코드'])
    stock_2 = list(before_stock_2['종목코드'])
    stock_3 = list(before_stock_3['종목코드'])

    for index, row in sector_stk.iterrows():
        if row['종목코드'] in stock_1:
            one_before_end_price = before_stock_1[before_stock_1['종목코드'] == row['종목코드']]['시작일 기준가'].iloc[0]
            one_before_end_rate = before_stock_1[before_stock_1['종목코드'] == row['종목코드']]['등락률'].iloc[0]
        else:
            one_before_end_price = None
            one_before_end_rate = None

        if row['종목코드'] in stock_2:
            two_before_end_price = before_stock_2[before_stock_2['종목코드'] == row['종목코드']]['시작일 기준가'].iloc[0]
            two_before_end_rate = before_stock_2[before_stock_2['종목코드'] == row['종목코드']]['등락률'].iloc[0]
        else:
            two_before_end_price = None
            two_before_end_rate = None

        if row['종목코드'] in stock_3:
            three_before_end_price = before_stock_3[before_stock_3['종목코드'] == row['종목코드']]['시작일 기준가'].iloc[0]
            three_before_end_rate = before_stock_3[before_stock_3['종목코드'] == row['종목코드']]['등락률'].iloc[0]
        else:
            three_before_end_price = None
            three_before_end_rate = None

        
        data = {
            'prdt_cd' : row['종목코드'],
            'prdt_name' : row['종목명'],
            'end_price' : row['종가'],
            'fluctuation_rate' : row['등락률'],
            'trade_amount' : row['거래량'],
            'trade_price_amount' : row['거래대금'],
            'capitalization' : row['시가총액'],
            'shared_amount' : row['상장주식수'],
            'idx_bztp_mcls_cd_name' : business_stk[business_stk['종목코드'] == row['종목코드']]['업종명'].iloc[0] if not business_stk.empty else None,
            'one_before_end_price' : one_before_end_price,
            'one_before_end_rate' : one_before_end_rate,
            'two_before_end_price' : two_before_end_price,
            'two_before_end_rate' : two_before_end_rate,
            'three_before_end_price' : three_before_end_price,
            'three_before_end_rate' : three_before_end_rate,
        }

        stock_serializer = StockSerializer(data = data)
        if stock_serializer.is_valid(raise_exception=True):
            stock_serializer.save()

    return HttpResponse('금융 상품 API 요청 완료')

@api_view(['GET'])
def create_dummy_data(request):
    make_data.make_data()
    return HttpResponse('포트폴리오 기초 데이터 생성 완료')

@api_view(['GET'])
def create_dummy_data2(request):
    make_data2.make_data()
    return HttpResponse('분석 데이터 생성 완료')

@api_view(['GET', 'POST'])
def deposit_list(request):
    if request.method == 'GET':
        deposits = get_list_or_404(DepositProduct)
        serializer = DepositProductSerializer(deposits, many=True)
        return Response(serializer.data)
    else:
         # __contain = @, @가 포함된 
        deposits = DepositProduct.objects.filter(fin_prdt_nm__contains = request.data.get('term'))
        serializer = DepositProductSerializer(deposits, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def saving_list(request):
    if request.method == 'GET':
        savings = get_list_or_404(SavingProduct)
        serializer = SavingProductSerializer(savings, many=True)
        return Response(serializer.data)
    else:
        # __contain = @, @가 포함된
        savings = SavingProduct.objects.filter(fin_prdt_nm__contains = request.data.get('term'))
        serializer = SavingProductSerializer(savings, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def stock_list(request):
    if request.method == 'GET':
        stocks = get_list_or_404(StockProduct)
        serializers = StockSerializer(stocks, many=True)
        return Response(serializers.data)
    else:
        # __contain = @, @가 포함된 
        stocks = StockProduct.objects.filter(prdt_name__contains = request.data.get('term'))
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def get_finance_corporation_name_list(request):
    serializer = FinanceCorportaionNameSerializer()
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def my_portfolio(request):
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), username=request.data.get('username'))
        portfolio_base = PortfolioBase.objects.get(user=user)
        portfolio = Portfolio.objects.get(user=user)

        serializer_pb = PortfolioBaseSerializer(portfolio_base)
        serializer_deposit = DepositProductJoinInfoSerializer(portfolio.deposit, many=True)
        serializer_saving = SavingProductJoinInfoSerializer(portfolio.saving, many=True)
        serializer_stock = StockProductBuyInfoSerializer(portfolio.stock, many=True)

        serializer = {
            'portfolio_base': serializer_pb.data,
            'deposits': serializer_deposit.data,
            'savings': serializer_saving.data,
            'stocks': serializer_stock.data,  
        }
        return Response(serializer)
    
@api_view(['GET'])
def get_user_product_list(request):
    file_path = f'{base_dir}/accounts/fixtures/accounts/'

    my_data_json = pd.read_json(f'{file_path}/user_product_data.json').T
    portfolio_data = json_normalize(my_data_json['portfolio_base']).reset_index()
    deposit_data = json_normalize(my_data_json['deposits'])
    saving_data = json_normalize(my_data_json['savings'])
    stock_data = json_normalize(my_data_json['stocks'])

    # 적금
    deposit_data_expand = pd.DataFrame()
    for index, col in enumerate(deposit_data.columns):
        index += 1
        tmp = json_normalize(deposit_data[col])
        tmp.columns = [f'fin_prdt_nm{index}', f'rate{index}', f'rate_prime{index}',f'save_trm{index}']
        deposit_data_expand = pd.concat([deposit_data_expand, tmp], axis=1)

    # 상품들을 하나의 리스트로 저장
    deposit_data_expand['deposit'] = deposit_data_expand.apply(lambda row: [row['fin_prdt_nm1'], row['fin_prdt_nm2'], row['fin_prdt_nm3']], axis=1)
    # # user, stock 데이터 병합
    user_product_data = pd.merge(portfolio_data, deposit_data_expand[['deposit']].reset_index(), on='index')
    # 각 값을 하나의 행으로 분리
    user_product_data = user_product_data.explode('deposit', ignore_index=True)

    # 예금 
    saving_data_expand = pd.DataFrame()
    for index, col in enumerate(saving_data.columns):
        index += 1
        tmp = json_normalize(saving_data[col])
        tmp.columns = [f'fin_prdt_nm{index}', f'rate{index}', f'rate_prime{index}',f'save_trm{index}']
        saving_data_expand = pd.concat([saving_data_expand, tmp], axis=1)

    # 상품들을 하나의 리스트로 저장
    saving_data_expand['saving'] = saving_data_expand.apply(lambda row: [row['fin_prdt_nm1'], row['fin_prdt_nm2'], row['fin_prdt_nm3']], axis=1)
    tmp = saving_data_expand.explode('saving', ignore_index=True)
    user_product_data = pd.concat([user_product_data, tmp['saving']], axis=1)

    # 주식 
    stock_data_expand = pd.DataFrame()
    for index, col in enumerate(stock_data.columns):
        index += 1
        tmp = json_normalize(stock_data[col])
        tmp.columns = [f'prdt_name{index}', f'idx_bztp_mcls_cd_name{index}']
        stock_data_expand = pd.concat([stock_data_expand, tmp], axis=1)

    # 상품들을 하나의 리스트로 저장
    stock_data_expand['stock'] = stock_data_expand.apply(lambda row: [row['prdt_name1'], row['prdt_name2']], axis=1)
    tmp = stock_data_expand.explode('stock', ignore_index=True)
    user_product_data = pd.concat([user_product_data, tmp['stock']], axis=1)
    data = user_product_data[['deposit', 'saving', 'stock']].fillna('None')

    json_str = data.to_json(orient='records', force_ascii=False)
    json_data = json.loads(json_str)

    # JsonResponse로 반환
    return JsonResponse({'result': json_data}, safe=False)

@api_view(['GET'])
def get_exchange_rates(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    rates = []

    for i in range(30):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        year, month, day = date.split('-')
        url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/history/{year}/{month}/{day}/KRW'
        # url = f'https://v6.exchangerate-api.com/v6/3054662f584c626227ad0023/history/2024/05/22/KRW'
        response = requests.get(url)
        print(response)
        data = response.json()
        print(data)
        # rates.append(data['rates'].get(currency, None))

    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

    # 그래프 생성
    plt.figure(figsize=(10, 5))
    plt.plot(dates, rates, marker='o')
    plt.xlabel('Date')
    plt.ylabel(f'Exchange Rate (KRW/)')
    plt.title(f'30-Day Exchange Rate for KRW')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 이미지를 메모리에 저장
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()

    # 이미지 데이터를 base64로 인코딩
    graph_base64 = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return HttpResponse(graph_base64, content_type='text/plain')
