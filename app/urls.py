from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='welcome-index'),
    path('login/', views.login, name='account-auth-token'),
    path('logout/', views.logout, name='account-auth-logout'),
    path('request-otp/', views.otp_request, name='account-request-otp'),
    path('verify-otp/', views.otp_verify, name='account-verify-otp'),
    path('banks/', views.BankDetails.as_view(), name='banks'),
    path('users/', views.UserDetails.as_view(), name='users'),
    path('ec-status/', views.EcStatusAPI.as_view(), name='ec-status-all'),
    path('customer-counts/', views.VerificationQuotaAPI.as_view(), name='customer-counts'),
    path('time-reports/', views.ReportsAPI.as_view(), name='time-reports')
]