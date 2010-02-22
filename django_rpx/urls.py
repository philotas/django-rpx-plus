from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views as auth_views

#import django_rpx.views

urlpatterns = patterns('django_rpx.views',
    #url(r'^activate/complete/$',
    #    direct_to_template,
    #    { 'template': 'registration/activation_complete.html' },
    #    name='registration_activation_complete'),
    url(r'^$', 'home', name='auth_home'),
    url(r'^rpx_response/$', 'rpx_response', name='rpx_response'),
    url(r'^login/$', 'login', name='auth_login'),
    url(r'^register/$', 'register', name='auth_register'),
    #It's up to user to implement this.
    #url(r'^profile/$', 'profile', name='auth_profile'),
    url(r'^associate/$', 'associate', name='auth_associate'),
    url(r'^associate/rpx_response/$', 'associate_rpx_response', name='associate_rpx_response'),
    url(r'^logout/$', auth_views.logout, 
                      {'template_name': 'registration/logged_out.html'}, 
                      name='auth_logout'),
)
