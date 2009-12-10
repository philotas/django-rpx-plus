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
    #RPX sends token back via POST
    token = request.POST.get('token', False)
    if not token: return HttpResponseForbidden()

    #See if a redirect param is specified. params are sent via both POST and
    #GET. If not, we will default to LOGIN_REDIRECT_URL.
    try:
        destination = request.POST['next']
    except KeyError:
        destination = settings.LOGIN_REDIRECT_URL
    
    #Since we specified the rpx auth backend in settings, this will use our
    #custom authenticate function.
    user = authenticate(token = token)
    if user:
        if user.is_active:
            #login creates session for the user.
            login(request, user)
            return HttpResponseRedirect(destination)
        else:
            #User is not active. There is a possibility that the user is new
            #and needs to be registered/associated. We check that here. First,
            #get associated RpxData. Since we created a new dummy user for this
            #new Rpx login, we *know* that there will only be one RpxData
            #associated to this dummy user. If no RpxData exists for the user,
            #or if is_associated is True, then we assume that the User has
            #been deactivated.
            try:
                user_rpxdata = RpxData.objects.get(user = user)
                if user_rpxdata.is_associated == False:
                    #Okay! This means that we have a new user waiting to be
                    #associated to an account!
                    #TODO: Make this redirec to register url.
                    return HttpResponseRedirect(destination)
            except RpxData.DoesNotExist:
                #Do nothing, auth has failed.
                pass

    
    #If no user object is returned, then authentication has failed.
    return HttpResponseForbidden()
