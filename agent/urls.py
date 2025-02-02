from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='agent-index'),
    path('login/', views.index, name='agent-index-redirect'),
    path('me/', views.get_me, name='agent-me'),
    path('customer-registration/', views.CustomerRegistration.as_view(), name='agent-customer-registration'),
    path('get-verification-status/', views.CustomerVerificationStatus.as_view(), name='agent-customer-verification-status'),
    path('get-verification-log/', views.CustomersVerificationLog.as_view(), name='agent-customers-verification-log'),
    path('liveliness/', views.liveliness_check, name='liveliness-check'),
    url(r'^.*/$', views.index, name='agent-redirect')
]