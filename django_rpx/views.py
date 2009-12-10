from django.conf import settings
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from django_rpx.models import RpxData
from django_rpx.forms import RegisterForm

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
    user = auth.authenticate(token = token)
    if user:
        if user.is_active:
            #login creates session for the user.
            auth.login(request, user)
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
                    #TODO: Make sure we really need to login here...
                    auth.login(request, user)
                    return HttpResponseRedirect(settings.REGISTER_URL+\
                                                '?next='+destination)
            except RpxData.DoesNotExist:
                #Do nothing, auth has failed.
                pass

    
    #If no user object is returned, then authentication has failed.
    return HttpResponseForbidden()

#TODO: Just render this template in urls.py
def login(request):
    return render_to_response('django_rpx/login.html', {
                              })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print data

            #Now modify the "dummy" user we created with the new values
            request.user.username = data['username']
            request.user.email = data['email']
            request.user.is_active = True
            request.user.save()
            #Also, indicate in the user associated RpxData that the login has
            #been associated with a username.
            user_rpxdata = RpxData.objects.get(user = request.user)
            user_rpxdata.is_associated = True
            user_rpxdata.save()

            #Return to show page
            return HttpResponse('success')
            #return HttpResponseRedirect(reverse('auth_profile'))
    else: 
        #Try to pre-populate the form with data gathered from the RPX login.
        try:
            user_rpxdata = RpxData.objects.get(user = request.user)
            profile = user_rpxdata.profile
            form = RegisterForm(initial = {
                'username': profile.get('preferredUsername') or \
                            profile.get('displayName'),
                'email': profile.get('email', '')
            })
        except RpxData.DoesNotExist:
            form = RegisterForm()

    return render_to_response('django_rpx/register.html', {
                                'form': form,
                              })
