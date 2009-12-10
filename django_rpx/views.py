from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings

from django_rpx.models import RpxData

def permute_name(name_string, num):
    num_str=str(num)
    max_len=29-len(num_str)
    return ''.join([name_string[0:max_len], '-', num_str])

def rpx_response(request):
    #Get the token from either POST or GET
    token = request.POST.get('token', False) 
    if not token:
        token = request.GET.get('token', False)
    if not token: return HttpResponseForbidden()
    
    #Since we specified the rpx auth backend in settings, this will use our
    #custom authenticate function.
    user = authenticate(token = token)
    if user and user.is_active:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        return HttpResponseForbidden()
