"""ekyc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static, serve
from app.views import not_found
from gflow.views import GFlowRenderView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.generic import RedirectView


@api_view(['GET'])
def protected_serve(request, path, document_root=None, show_indexes=False):
    if request.user.is_authenticated:
        return serve(request, path, document_root, show_indexes)
    return HttpResponse('not found')

admin.site.site_header = "Giga-Ekyc Admin"
admin.site.site_title = "Giga-Ekyc Admin Portal"
admin.site.index_title = "Welcome to Giga-Ekyc Admin"


# urlpatterns = [

#     path('', admin.site.urls), 
#     path('404/', not_found, name='404-not-found'),
#     path('app/', include('app.urls')),
#     path('bank/', include('bank.urls')),
#     path('agent/', include('agent.urls')),
#     path('customer/', include('customer.urls')),
#     path('gflow/', include('gflow.urls')),
#     re_path(r'^onboarding/$', GFlowRenderView.as_view(), name='gflow-rendering-index'),
#     re_path(r'^onboarding/(?P<page>[\w\-]+)/$', GFlowRenderView.as_view(), name='gflow-rendering-customer'),
#     # re_path(r'^onboarding/(?P<page>[\w\-]+)/(?P<cpk>\d+)/$', GFlowRenderView.as_view(), name='gflow-rendering-agent'),
#     url(r'^%s(?P<path>.*)$' % settings.SECURE_FILE_URL[1:], protected_serve, {'document_root': settings.NID_UPLOAD_DIR}),
# ]


urlpatterns = []

urlpatterns.extend([url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),])

if settings.ACCESS_CHANNEL == 'api_only':
    urlpatterns.extend([path('admin/', admin.site.urls),
    path('404/', not_found, name='404-not-found'),
    path('app/', include('app.urls')),
    path('bank/', include('bank.urls')),
    path('agent/', include('agent.urls')),
    url(r'^%s(?P<path>.*)$' % settings.SECURE_FILE_URL[1:], protected_serve, {'document_root': settings.NID_UPLOAD_DIR})])
else:
    if settings.ACCESS_CHANNEL == 'bankled' or settings.ACCESS_CHANNEL == 'all':
        urlpatterns.extend([path('admin/', admin.site.urls),
        path('404/', not_found, name='404-not-found'),
        path('app/', include('app.urls')),
        path('bank/', include('bank.urls')),
        path('agent/', include('agent.urls')),
        # path('customer/', include('customer.urls')),
        path('gflow/', include('gflow.urls')),])

    urlpatterns.extend([
        url(r'^%s(?P<path>.*)$' % settings.SECURE_FILE_URL[1:], protected_serve, {'document_root': settings.NID_UPLOAD_DIR}),
        re_path(r'(?P<app>.*)/$', GFlowRenderView.as_view(), name='gflow-rendering-any'),
        path('', GFlowRenderView.as_view(), name='gflow-rendering-index')
    ])