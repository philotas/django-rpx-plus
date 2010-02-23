from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^example/', include('example.foo.urls')),

    #url(r'^', include('example.urls')),
    # Account/Auth URLs not implemented by django_rpx:
    url(r'^accounts/$', 'django.views.generic.simple.redirect_to', 
                        {'url': '/accounts/profile/', 'permanent': False},
                        name='auth_home'),
    url(r'^accounts/profile/$', 'app.views.profile', name='auth_profile'),
    #We will use django's built in logout view.
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
                      {'template_name': 'registration/logged_out.html'}, 
                      name='auth_logout'),

    # For django_rpx
    (r'^accounts/', include('django_rpx.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
