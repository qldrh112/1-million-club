from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import PortfolioBaseSerializer
from .models import *
from .make_data import banks, industries

from pandas import json_normalize
import pandas as pd
import numpy as np
import pickle
import os

base_dir = settings.BASE_DIR

@api_view(['GET', 'POST'])
def portfolio(request):
    if request.method == 'GET':
        pass
    else:
        # 머신러닝 (분류)
        save_dir = os.path.join(os.getcwd(), 'accounts', 'weights')

        # 모델 path
        deposit_model_path = os.path.join(save_dir, 'lgbm_deposit.pkl')
        saving_model_path = os.path.join(save_dir, 'lgbm_saving.pkl')
        stock_model_path = os.path.join(save_dir, 'lgbm_stock.pkl')
        # 인코더 path
        co_nm_endcoder_path = os.path.join(save_dir, 'le_co_nm.pkl')
        industry_endcoder_path = os.path.join(save_dir, 'le_industry.pkl')

        # 모델 로드
        with open(deposit_model_path, 'rb') as f:
            deposit_model = pickle.load(f)
        with open(saving_model_path, 'rb') as f:
            saving_model = pickle.load(f)
        with open(stock_model_path, 'rb') as f:
            stock_model = pickle.load(f)

        # 인코더 로드
        with open(co_nm_endcoder_path, 'rb') as f:
            co_nm_encoder = pickle.load(f)
        with open(industry_endcoder_path, 'rb') as f:
            industry_encoder = pickle.load(f)
    
        # 데이터 선언
        seed_money = int(request.data['seed_money'])
        invest_aggresive = int(request.data['invest_aggresive'])
        invest_conservative = 100 - int(invest_aggresive)
        salary = int(request.data['salary'])
        age = int(request.data['age']) // 10
        kor_co_nm = co_nm_encoder.transform([request.data['kor_co_nm']])
        industry = industry_encoder.transform([request.data['industry']])

        if seed_money < 15000000:
            income_bracket = 1
        elif seed_money < 24000000:
            income_bracket = 2
        elif seed_money < 34000000:
            income_bracket = 3
        elif seed_money < 46000000:
            income_bracket = 4
        else:
            income_bracket = 5

        new_data = np.array([[seed_money, invest_aggresive, invest_conservative, salary, age, int(kor_co_nm[0]), int(industry[0]), income_bracket]])

        # 예측
        deposit_predict = deposit_model.predict(new_data)
        saving_predict = saving_model.predict(new_data)
        stock_predict = stock_model.predict(new_data)

        # to_json
        best_recommend = {
            '예금':deposit_predict[0],
            '적금':saving_predict[0],
            '주식':stock_predict[0],
        }

        file_path = os.path.join(os.getcwd(), 'accounts', 'fixtures','accounts')

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

        # 연령대 생성
        def age_range(age):
            if age < 30:
                return 2
            elif age < 40:
                return 3
            elif age < 50:
                return 4
            elif age < 60:
                return 5
            elif age < 70:
                return 6
            else:
                return 7
        user_product_data['age_range'] = user_product_data['age'].apply(age_range)

        # 적금 추천
        recommend_deposit = list(user_product_data[(user_product_data['age_range'] == age) & (user_product_data['income_bracket'] == income_bracket)]['deposit'].value_counts()[:3].index)
        if not recommend_deposit:
            recommend_deposit = list(user_product_data[user_product_data['income_bracket'] == income_bracket]['deposit'].value_counts()[:3].index)

        # 예금추천
        recommend_saving = list(user_product_data[(user_product_data['age_range'] == age) & (user_product_data['income_bracket'] == income_bracket)]['saving'].value_counts()[:3].index)
        if not recommend_saving:
            recommend_saving = list(user_product_data[user_product_data['income_bracket'] == income_bracket]['saving'].value_counts()[:3].index)

        # 주식추천
        recommend_stock = list(user_product_data[(user_product_data['age_range'] == age) & (user_product_data['industry'] == request.data['industry'])]['stock'].value_counts()[:3].index)
        if not recommend_stock:
            recommend_stock = list(user_product_data[user_product_data['industry'] == request.data['industry']]['stock'].value_counts()[:3].index)

        filter_recommend = {
            '예금':recommend_deposit,
            '적금':recommend_saving,
            '주식':recommend_stock,
        }

        data = {'value': {'best_recommend' : best_recommend, 'filter_recommend' : filter_recommend}}

        return JsonResponse(data)


@api_view(['GET'])
def bank_list(request):
    return Response(banks())


@api_view(['GET'])
def industry_list(request):
    return Response(industries())
