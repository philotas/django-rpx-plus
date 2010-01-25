from django import template
from django.template import Context, loader
from django.template.loader import render_to_string
import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
from django.utils.http import urlencode

"""
"rpx_tags" is a slightly redundant name, but if I call this module simple
"rpx" it only allows me to use the first tag found (although all tags appear
in the libary)

weird.

Anyway.

TODO:
  * provide for language choice
  * document
  * provide for customisation for the "overlay" attribute, whatever it is.

"""

register = template.Library()

@register.inclusion_tag('django_rpx/rpx_link.html')
def rpx_link(text, extra = None, rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site=Site.objects.get_current()

    if extra != None:
        extra = '?'+urlencode(extra)

    return {
        'text': text,
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" % (current_site.domain, 
                                        rpx_response,
                                        extra)
    }

@register.inclusion_tag('django_rpx/rpx_script.html')
def rpx_script(extra = None, rpx_response = reverse('django_rpx.views.rpx_response'), flags = ''):
    '''
    Arguments to flag will go into the RPXNOW.flags = '' var. A good use case 
    would be to set flags = 'show_provider_list' to force showing all login providers
    even if user is logged in.
    '''
    current_site = Site.objects.get_current()

    if extra != None:
        extra = '?'+urlencode(extra)

    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" %(current_site.domain,
                                       rpx_response,
                                       extra),
        'flags': flags,
    }

@register.inclusion_tag('django_rpx/rpx_embed.html')
def rpx_embed(extra = None, rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site = Site.objects.get_current()

    if extra != None:
        extra = '?'+urlencode(extra)

    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" %(current_site.domain,
                                       rpx_response,
                                       extra)
    }

@register.inclusion_tag('django_rpx/rpx_url.html')
def rpx_url(extra = None, rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site = Site.objects.get_current()

    if extra != None:
        extra = '?'+urlencode(extra)

    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" %(current_site.domain,
                                       rpx_response,
                                       extra)
    }
