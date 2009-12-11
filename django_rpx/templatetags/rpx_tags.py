from django import template
from django.template import Context, loader
from django.template.loader import render_to_string
import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
"""
"rpx_tags" is a slightly redundant name, but if i clall this module simple "rpx" it only allows me to use the first tag found (although all tags appear in the libary)

weird.

Anyway.

TODO:
  * provide for language choice
  * document
  * provide for customisation for the "overlay" attribute, whatever it is.

"""

register = template.Library()

@register.inclusion_tag('django_rpx/rpx_link.html')
def rpx_link(text, extra = '', rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site=Site.objects.get_current()
    return {
        'text': text,
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" % (current_site.domain, 
                                        rpx_response,
                                        extra)
    }

@register.inclusion_tag('django_rpx/rpx_script.html')
def rpx_script(extra = '', rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site=Site.objects.get_current()
    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" %(current_site.domain,
                                       rpx_response,
                                       extra)
    }

@register.inclusion_tag('django_rpx/rpx_embed.html')
def rpx_embed(extra = '', rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site=Site.objects.get_current()
    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" %(current_site.domain,
                                       rpx_response,
                                       extra)
    }

@register.inclusion_tag('django_rpx/rpx_url.html')
def rpx_url(extra = '', rpx_response = reverse('django_rpx.views.rpx_response')):
    current_site=Site.objects.get_current()
    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': "http://%s%s%s" %(current_site.domain,
                                       rpx_response,
                                       extra)
    }
