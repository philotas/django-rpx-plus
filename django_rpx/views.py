from django.conf import settings
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
from django.utils.http import urlencode

# The messages framework will only be available from django 1.2 onwards. Since
# most people are still using <= 1.1.1, we fallback on the backported message
# framework:
try:
    from django.contrib import messages
except ImportError:
    import django_messages_framework as messages #backport of messages framework

from django_rpx.models import RpxData
from django_rpx.forms import RegisterForm

import re #for sub in register

#The primary ID to the RpxData object is set in session when user is logged in
#but not registered. The register view checks and uses this session var.
RPX_ID_SESSION_KEY = '_rpxdata_id'

def rpx_response(request):
    if request.method == 'POST':
        #According to http://rpxwiki.com/Passing-state-through-RPX, the query
        #string parameters in our token url will be POST to our rpx_response so
        #that we can retain some state information. We use this for 'next', a
        #var that specifies where the user should be redirected after successful
        #login.
        destination = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
            
        #RPX also sends token back via POST. We pass this token to our RPX auth
        #backend which, then, uses the token to access the RPX API to confirm 
        #that the user logged in successfully and to obtain the user's login
        #information.
        token = request.POST.get('token', False)
        if token: 
            response = auth.authenticate(token = token)
            #The django_rpx auth backend can return three things: None (means
            #that auth has failed), a RpxData object (means that user has passed
            #auth but is not registered), or a User object (means that user is
            #auth AND registered).
            #TODO: Use type(user) == User or RpxData to check.
            if type(response) == User:
                #Successful auth and user is registered so we login user.
                auth.login(request, response)
                return redirect(destination)
            elif type(response) == RpxData:
                #Successful auth, but user is NOT registered! So we redirect
                #user to the register page. However, in order to tell the
                #register view that the user is authed but not registered, 
                #we set a session var that points to the RpxData object 
                #primary ID. After the user has been registered, this session
                #var will be removed.
                request.session[RPX_ID_SESSION_KEY] = response.id
                #For security purposes, there could be a case where user 
                #decides not to register but then never logs out either. 
                #Another person can come along and then use the REGISTER_URL
                #to continue creating the account. So we expire this session
                #after a set time interval. (Note that this session expiry
                #setting will be cleared when user completes registration.)
                request.session.set_expiry(60 * 10) #10 min

                query_params = urlencode({'next': destination})
                return redirect(settings.REGISTER_URL+'?'+query_params)
            else:
                #Do nothing, auth has failed.
                pass

    #Authentication has failed. We'll send user  back to login page where error
    #message is displayed.
    messages.error(request, 'There was an error in signing you in. Try again?')
    query_params = urlencode({'next': destination})
    return redirect(reverse('auth_login')+'?'+query_params)

def associate_rpx_response(request):
    #See if a redirect param is specified. params are sent via both POST and
    #GET. If not, we will default to LOGIN_REDIRECT_URL.
    try:
        destination = request.POST['next']
        if destination.strip() == '':
            raise KeyError
    except KeyError:
        destination = reverse('auth_associate')

    #RPX sends token back via POST
    token = request.POST.get('token', False)
    if token: 
        #Since we specified the rpx auth backend in settings, this will use our
        #custom authenticate function.
        user = auth.authenticate(token = token)
        #Here are our cases:
        # user  user.is_active  ->  case
        #  T          T         ->  valid login, already associated
        #  T          F         ->  valid login, not associated
        #  F          T         ->  impossible case
        #  F          F         ->  in-valid login
        if user:
            if not user.is_active: #means non-associated, valid account 
                try:
                    user_rpxdata = RpxData.objects.get(user = user)
                    assert user_rpxdata.is_associated == False

                    #Associating the login. First, delete the dummy user:
                    user.delete()
                    #Now point the user foreign key on user_rpxdata:
                    user_rpxdata.user = request.user
                    #Set associated flag
                    user_rpxdata.is_associated = True
                    user_rpxdata.save()

                    #Set success message
                    messages.success(request, 'We successfully associated your new login with this account!')
                    
                    #The destination is most likely /accounts/associate/
                    return redirect(destination)
                except RpxData.DoesNotExist:
                    #Shouldn't happen since we needed to store the rpx data in
                    #order to auth the user.
                    messages.error(request, 'Unfortunately, we were unable to associate your new login with your current account. Try again?')
            else: #user.is_active = True; means already associated acct
                messages.error(request, 'Sorry, this login has already been associated with an existing account.')
        else: 
            #Rare that we'd get here. Means that we didn't send the right token or 
            #RPX had some server error in returning user info from the token we
            #sent.
            messages.error(request, 'There was an error in accessing your new login information. Try again?')
    else:
        #Means that user canceled the auth process or there was a sign-in error.
        messages.error(request, 'Unsuccessful login. Try again?')

    #Getting here means that the 
    return redirect(destination)

def login(request):
    next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    extra = {'next': next}

    return render_to_response('django_rpx/login.html', {
                                'extra': extra,
                              },
                              context_instance = RequestContext(request))

def register(request):
    #See if a redirect param is specified. If not, we will default to
    #LOGIN_REDIRECT_URL.
    next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)

    #In order to use register, user MUST have the session var RPX_ID_SESSION_KEY
    #set to the user's RpxData object. This indicates that the user has
    #successfully logged in via RPX but has not previously registered.
    try:
        rpxdata_id = request.session[RPX_ID_SESSION_KEY]
        #Check to see if this id exists
        rd = RpxData.objects.get(id = rpxdata_id)
    except (KeyError, RpxData.DoesNotExist):
        return redirect(next)
    
    #Check form submission.
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print data
            
            #We create the new user object and associate it with our RpxData
            #object:
            u = User()
            u.username = data['username']
            u.email = data['email']
            u.save()

            rd.user = u
            rd.save()

            #Now we log the user in. This also clears out the previous session
            #containing the expiring RPX_ID_SESSION_KEY var. Normally, we get
            #the user directly from auth.authenticate(...) which adds a
            #User.backend attribute. We have to manually add it here:
            u.backend = 'django_rpx.backends.RpxBackend'
            auth.login(request, u)

            return redirect(next)
    else: 
        #No form submission so we will display page with initial form data.
        #We try to pre-populate the form with data from the RPX login.
        rpx_profile = rd.profile

        #Clean the username to allow only alphanum and underscore.
        username =  rpx_profile.get('preferredUsername') or \
                    rpx_profile.get('displayName')
        username = re.sub(r'[^\w+]', '', username)

        form = RegisterForm(initial = {
            'username': username,
            'email': rpx_profile.get('email', '')
        })

    return render_to_response('django_rpx/register.html', {
                                'form': form,
                              },
                              context_instance = RequestContext(request))

def associate(request):
    if not request.user.is_authenticated() or not request.user.is_active:
        return redirect('auth_login')

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

def delete_associated_login(request, rpxdata_id):
    #TODO: Should use auth decorator instead of this:
    if not request.user.is_authenticated() or not request.user.is_active:
        return redirect('auth_login')

    #Check to see if the rpxdata_id exists and is associated with this user
    try:
        #We only allow deletion if user has more than one login
        num_logins = RpxData.objects.filter(user = request.user).count()
        if num_logins > 1:
            r = RpxData.objects.get(id = rpxdata_id, user = request.user)

            #Set success message.
            messages.success(request, 'Your '+r.provider+' login was successfully deleted.')

            #Actually delete
            r.delete()
    except RpxData.DoesNotExist:
        #Silent error, just redirect since message framework can't handle errors
        #yet.
        pass

    return redirect('auth_associate')
