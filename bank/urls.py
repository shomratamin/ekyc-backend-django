from django.urls import path
from django.views.generic.base import RedirectView
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='bank-welcome-index'),
    path('me/', views.get_me, name='bank-me'),
    path('kyc-params/', views.BankSettings.as_view(), name='kyc-params'),
    path('bank-settings/', views.BankSettings.as_view(), name='bank-settings'),
    path('branches/', views.BranchDetails.as_view(), name='bank-branches'),
    path('agents/', views.AgentDetails.as_view(), name='bank-customers'),
    path('email-new-password/', views.reset_password_and_send_in_email, name='bank-email-password'),
    # path('customers/', views.CustomerDetails.as_view(), name='bank-customers'),
    path('kyc-data-source/', views.KycDataSourceDetails.as_view(), name='bank-kyc-data-source'),
    path('ec-notification/', views.ec_notification, name='bank-ec-notification'),
    path('get-verification-status/', views.CustomerVerificationStatus.as_view(), name='bank-customer-verification-status'),
    path('get-verification-log/', views.CustomersVerificationLog.as_view(), name='bank-customers-verification-log'),
    path('customer-list/', views.CustomerList.as_view(), name='bank-customer-list'),
    path('customer-profile/', views.CustomerProfileView.as_view(), name='bank-customer-profile'),
    path('update-customer-bank-account/', views.CustomerBankAccount.as_view(), name='update-customer-bank-account'),
    path('retry-all-customers-verification/', views.CustomersVerificationRetry.as_view(), name='bank-customers-verification-retry-all'),
    url(r'^.*/$', views.index, name='bank-redirect')

]