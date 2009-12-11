from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django_rpx.models import RpxData
from django.conf import settings
from django_rpx.views import permute_name

import hashlib #encryption (MD5)
import time #for seeding

TRUSTED_PROVIDERS=set(getattr(settings,'RPX_TRUSTED_PROVIDERS', []))

class RpxBackend:
    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get_user_by_rpx_id(self, rpx_id):
        try:
            rd = RpxData.objects.get(identifier = rpx_id)
        except RpxData.DoesNotExist:
            return None
        return rd.user

    def authenticate(self, token=''):
        """
        TODO: pass in a message array here which can be filled with an error
        message with failure response
        """
        from django.utils import simplejson
        import urllib
        import urllib2

        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
          'format': 'json',
          'apiKey': settings.RPXNOW_API_KEY,
          'token': token
        }
        r = urllib2.urlopen(url=url,
          data=urllib.urlencode(args),
        )
        json = simplejson.load(r)

        #Login is successful ONLY if stat == 'ok'
        if json['stat'] != 'ok':
            #TODO: Check for why we have failure. See https://rpxnow.com/docs
            #      for the error codes.
            return None
        #At this point, we assume that the RPX authentication has been
        #successful. So no matter what, we will return a User object.
        
        #We can obtain user information for as long as the token is active
        #(which is 10 minutes). Since token has a short life-time, it's a good
        #idea to grab user information now and store it in database.
        #IDEA: Since we can have so much data that can be returned, we
        #shouldn't limit to a few fixed fields. We can either use a key-value
        #type store in a db table to store everything, or just store the
        #identifier and pass everything else off to a user defined function for
        #handling the extra data.
        profile = json['profile']
        rpx_id = profile['identifier'] #guaranteed
        provider = profile['providerName'] #guaranteed

        user = self.get_user_by_rpx_id(rpx_id)
        
        if not user:
            #No match, create a new user. We put in a dummy username.
            md5 = hashlib.md5()
            username = ''
            email = profile.get('email', '') #default to ''
            try:
                while True:
                    #Generate an md5 hash from time. We'll use this as our
                    #dummy username for now until user changes it.
                    md5.update(str(time.time())) #seeded with time
                    username = md5.hexdigest()
                    username = username[:30] #User.username max_length = 30
                    User.objects.get(username = username)
            except User.DoesNotExist:
                #available name!
                user = User.objects.create_user(username, email)
        
            #Since this is a new user, we do not active the user until the Rpx
            #login has been registered or have been really associated with the
            #new user account.
            user.is_active = False

            # Store the original nickname for display
            # TODO: We'll move this to the new user function/view
            # user.first_name = nickname
            user.save()

            rd = RpxData()
            rd.user = user
            rd.identifier = rpx_id
            rd.provider = provider
            rd.save()
        
        #Get associated RPX data and update it with our new provided data.
        #NOTE: Since our RPX table is now a one-to-many model (mapping one
        #user to many RPX datapoints), we need to think about how our user
        #data (non-identifier) is stored. The below is just a quick hack:
        rd = RpxData.objects.get(identifier = rpx_id)
        rd.profile = profile
        rd.save()

        return user
