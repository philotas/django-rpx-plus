from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.core.urlresolvers import reverse

from django_rpx.models import RpxData

def home(request):
    return HttpResponseRedirect(reverse('auth_home'))
    #return render_to_response('login.html', {
    #                          })

def success(request):
    #print request.POST

    #Get RPX data
    users_data = RpxData.objects.filter(user = request.user)
    
    return render_to_response('success.html', {
                                'users_data': users_data,
                              })
