from django.conf.urls.defaults import *

#import django_rpx.views

urlpatterns = patterns('django_rpx.views',
    url(r'^rpx_response/$', 'rpx_response', name='rpx_response'),
    url(r'^login/$', 'login', name='auth_login'),
    url(r'^register/$', 'register', name='auth_register'),
    url(r'^associate/$', 'associate', name='auth_associate'),
    url(r'^associate/rpx_response/$', 'associate_rpx_response', name='associate_rpx_response'),
)
