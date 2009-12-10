from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

#import django_rpx.views

urlpatterns = patterns('django_rpx.views',
    #url(r'^activate/complete/$',
    #    direct_to_template,
    #    { 'template': 'registration/activation_complete.html' },
    #    name='registration_activation_complete'),
    url(r'^rpx_response/$', 'rpx_response', name='rpx_response'),
    url(r'^login/$', 'login', name='auth_login'),
    url(r'^register/$', 'register', name='auth_register'),
    #url(r'^logout/$', 'logout', name='auth_logout'),
)
