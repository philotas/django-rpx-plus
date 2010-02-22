# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
#from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
# The messages framework will only be available from django 1.2 onwards. Since
# most people are still using <= 1.1.1, we fallback on the backported message
# framework:
try:
    from django.contrib import messages
except ImportError:
    import django_messages_framework as messages #backport of messages framework

from .forms import ProfileForm

def profile(request):
    #TODO: Should use auth decorator instead of this:
    if not request.user.is_authenticated() or not request.user.is_active:
        return redirect('auth_login')

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

    return render_to_response('app/profile.html', {
                                'form': form,
                                'message': message,
                                'user': request.user,
                              },
                              context_instance = RequestContext(request))
