from django.urls import path

from . import views

urlpatterns = [
    path('', views.GFlowIDEView.as_view(), name='gflow-index'),
    path('update-page/', views.GFlowPageEditView.as_view(), name='gflow-page-edit'),
]