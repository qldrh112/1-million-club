from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from accounts import make_data, make_data2
from .models import *
from .serializers import *
import FinanceDataReader as fdr
from rest_framework.authtoken.models import Token
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import pandas as pd
# import json
import re
from accounts.models import *
from accounts.serializers import *
from finances.serializers import *
from accounts.serializers import CustomPortfolioSerializer
from django.contrib.auth.hashers import make_password
import random
import requests
from datetime import datetime, timedelta
from finances.models import DepositProduct, SavingProduct, StockProduct, DepositOption, SavingOption
import json
from collections import OrderedDict

    


def make_data():
    N = 10000
    file = OrderedDict()

    user_data_save_dir = 'accounts/fixtures/accounts/test10000.json'
    for i in range(1, N+1):
        print(i)
        user = get_object_or_404(get_user_model(), id=i)
        portfolio_base = PortfolioBase.objects.get(user=user)
        portfolio = Portfolio.objects.get(user=user)

        serializer_pb = M_PortfolioBaseSerializer(portfolio_base)
        serializer_deposit = M_DepositProductJoinInfoSerializer(portfolio.deposit, many=True)
        serializer_saving = M_SavingProductJoinInfoSerializer(portfolio.saving, many=True)
        serializer_stock = M_StockProductBuyInfoSerializer(portfolio.stock, many=True)

        serializer = {
            'portfolio_base': serializer_pb.data,
            'deposits': serializer_deposit.data,
            'savings': serializer_saving.data,
            'stocks': serializer_stock.data,  
        }
        # 랜덤한 데이터를 삽입
        file[str(i)] = serializer

    with open(user_data_save_dir, 'w', encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent='\t')

    print(f'데이터 생성 완료 / 저장 위치: {user_data_save_dir}')


