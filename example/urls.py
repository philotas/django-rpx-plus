from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^example/', include('example.foo.urls')),

    url(r'^$', 'django.views.generic.simple.redirect_to', 
               {'url': '/accounts/profile/', 'permanent': False},
               name='home'),
    # Account/Auth URLs not implemented by django_rpx:
    url(r'^accounts/$', 'django.views.generic.simple.redirect_to', 
                        {'url': '/accounts/profile/', 'permanent': False},
                        name='auth_home'),
    url(r'^accounts/profile/$', 'app.views.profile', name='auth_profile'),
    #We will use django's built in logout view.
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
                      {'template_name': 'django_rpx/logged_out.html'}, 
                      name='auth_logout'),

    # For django_rpx
    (r'^accounts/', include('django_rpx.urls')),
    
    #For serving static files in dev environment.
    #See: http://docs.djangoproject.com/en/dev/howto/static-files/
    #In production setting, the webserver automatically overrides this, 
    #so there is no need to take this out when in production:
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
