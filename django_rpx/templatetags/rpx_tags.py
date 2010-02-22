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

def _rpx_common(request, extra = '', rpx_response = False):
    '''
    Common code for rpx_* template inclusion tags.
    '''
    if extra != '':
        extra = '?'+urlencode(extra)
    if not rpx_response:
        #This is the default rpx_response that will be used most of the time.
        #The only time when we don't use this, is when we need to associate
        #a login, so we end up using a different url.
        rpx_response = reverse('django_rpx.views.rpx_response')

    #Construct the token url:
    token_url = "http://%s%s%s" % (request.get_host(),
                                   rpx_response,
                                   extra)
    return {
        'realm': settings.RPXNOW_REALM,
        'token_url': token_url,
    }


@register.inclusion_tag('django_rpx/rpx_link.html', takes_context = True)
def rpx_link(context, text, extra = '', rpx_response = False):
    #NOTE: We have to manually specify each of the args; can't use *args,
    #**kwargs.
    common = _rpx_common(context['request'], extra, rpx_response)

    #Add link text to template var dict
    common['text'] = text

    return common

@register.inclusion_tag('django_rpx/rpx_script.html', takes_context = True)
def rpx_script(context, extra = '', rpx_response = False, flags = ''):
    '''
    Arguments to flag will go into the RPXNOW.flags = '' var. A good use case 
    would be to set flags = 'show_provider_list' to force showing all login providers
    even if user is logged in.
    '''
    common = _rpx_common(context['request'], extra, rpx_response)
    
    #Add additional template vars
    common['flags'] = flags

    return common


@register.inclusion_tag('django_rpx/rpx_embed.html', takes_context = True)
def rpx_embed(context, extra = '', rpx_response = False):
    common = _rpx_common(context['request'], extra, rpx_response)

    return common


@register.inclusion_tag('django_rpx/rpx_url.html', takes_context = True)
def rpx_url(context, extra = '', rpx_response = False):
    common = _rpx_common(context['request'], extra, rpx_response)

    return common
