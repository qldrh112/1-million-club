from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('finances/', include('finances.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/portfolio/', views.portfolio),
    path('accounts/banks/', views.bank_list),
    path('accounts/industries/', views.industry_list),
]