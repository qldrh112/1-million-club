from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create/data/', views.create_data), # 데이터 생성
    path('create/data/dummy/', views.create_dummy_data), # 더미데이터 생성
    path('create/data/dummy2/', views.create_dummy_data2), # 통합 더미데이터
    path('deposit/', views.deposit_list), # 적금정보
    path('saving/', views.saving_list), # 예금정보
    path('stock/', views.stock_list), # 주식정보
    path('myportfolio/', views.my_portfolio),
    path('user/product/', views.get_user_product_list), # 유저 - 금융 정보
    # path('search/corp/', views.corp_account_search), # 재무 정보 - 기업 데이터 입력 필요
    # path('kor_co_nm/', views.get_finance_corporation_name_list), # 기업 목록
    path('exchange-rates/', views.get_exchange_rates),
]
