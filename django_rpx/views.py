from django.conf import settings
import django.contrib.auth as auth
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
from django.utils.http import urlencode

#TODO: Catch exception, try to import real messages framework first.
import django_messages_framework as messages #backport of messages framework

from django_rpx.models import RpxData
from django_rpx.forms import RegisterForm, ProfileForm

import re #for sub in register

def permute_name(name_string, num):
    num_str=str(num)
    max_len=29-len(num_str)
    return ''.join([name_string[0:max_len], '-', num_str])

def rpx_response(request):
    #See if a redirect param is specified. params are sent via both POST and
    #GET. If not, we will default to LOGIN_REDIRECT_URL.
    try:
        destination = request.POST['next']
        if destination.strip() == '':
            raise KeyError
    except KeyError:
        destination = settings.LOGIN_REDIRECT_URL
        
    #RPX sends token back via POST
    token = request.POST.get('token', False)
    if token: 
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

    
    #If no user object is returned, then authentication has failed. We'll send
    #user to login page where error message is displayed.
    #Set success message.
    messages.error(request, 'There was an error in signing you in. Try again?')
    destination = urlencode({'next': destination})
    return HttpResponseRedirect(reverse('auth_login')+'?'+destination)

def associate_rpx_response(request):
    #See if a redirect param is specified. params are sent via both POST and
    #GET. If not, we will default to LOGIN_REDIRECT_URL.
    try:
        destination = request.POST['next']
        if destination.strip() == '':
            raise KeyError
    except KeyError:
        destination = settings.LOGIN_REDIRECT_URL

    #RPX sends token back via POST
    token = request.POST.get('token', False)
    if token: 
        #Since we specified the rpx auth backend in settings, this will use our
        #custom authenticate function.
        user = auth.authenticate(token = token)
        if user and not user.is_active:
            try:
                #Make sure this login hasn't been associated yet:
                user_rpxdata = RpxData.objects.get(user = user)
                if user_rpxdata.is_associated == False:
                    #Okay! This means that we can now associate this login. First,
                    #delete the dummy user:
                    user.delete()
                    #Now point the user foreign key on user_rpxdata:
                    user_rpxdata.user = request.user
                    #Set associated flag
                    user_rpxdata.is_associated = True
                    user_rpxdata.save()
                    
                    #The destination is most likely /accounts/associate/
                    return HttpResponseRedirect(destination)
            except RpxData.DoesNotExist:
                #Do nothing, auth has failed.
                pass
    
    #Getting here means that we don't have a login that hasn't been associated yet.
    #return HttpResponseForbidden()
    return render_to_response('django_rpx/associate_failed.html', {
                              },
                              context_instance = RequestContext(request))

def home(request):
    return HttpResponseRedirect(reverse('auth_profile'))

#TODO: Just render this template in urls.py
def login(request):
    next = request.GET.get('next', '/accounts/profile')
    extra = {'next': next}

    return render_to_response('django_rpx/login.html', {
                                'extra': extra,
                              },
                              context_instance = RequestContext(request))

def register(request):
    if request.method == 'POST':
        #See if a redirect param is specified. If not, we will default to
        #LOGIN_REDIRECT_URL.
        try:
            destination = request.GET['next']
            if destination.strip() == '':
                raise KeyError
        except KeyError:
            destination = settings.LOGIN_REDIRECT_URL

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

            return HttpResponseRedirect(destination)
    else: 
        #Try to pre-populate the form with data gathered from the RPX login.
        try:
            user_rpxdata = RpxData.objects.get(user = request.user)
            profile = user_rpxdata.profile

            #Clean the username to allow only alphanum and underscore.
            username =  profile.get('preferredUsername') or \
                        profile.get('displayName')
            username = re.sub(r'[^\w+]', '', username)

            form = RegisterForm(initial = {
                'username': username,
                'email': profile.get('email', '')
            })
        except RpxData.DoesNotExist:
            form = RegisterForm()

    return render_to_response('django_rpx/register.html', {
                                'form': form,
                              },
                              context_instance = RequestContext(request))

def associate(request):
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect(reverse('auth_login'))

    #Get associated accounts
    user_rpxdatas = RpxData.objects.filter(user = request.user)

    #We need to send the rpx_response to a customized method so we pass the
    #custom rpx_response path into template:
    return render_to_response('django_rpx/associate.html', {
                                'user': request.user, 
                                'user_rpxdatas': user_rpxdatas,
                                'num_logins': len(user_rpxdatas), 
                                'rpx_response_path': reverse('associate_rpx_response'),
                                'extra': {'next': reverse('auth_associate')},
                              },
                                  context_instance = RequestContext(request))

def profile(request):
    #TODO: Should use auth decorator instead of this:
    if not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseRedirect(reverse('auth_login'))

    message = False #A crude hack for displaying success messages
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print data

            #Update user with form data
            request.user.first_name = data['first_name']
            request.user.last_name = data['last_name']
            request.user.email = data['email']
            request.user.save()

            message = 'Successfully updated profile!'

            #Stay on profile page.
            #return HttpResponse('success')
    else: 
        #Try to pre-populate the form with user data.
        form = ProfileForm(initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render_to_response('django_rpx/profile.html', {
                                'form': form,
                                'message': message,
                                'user': request.user,
                              },
                              context_instance = RequestContext(request))
