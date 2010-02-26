from django.test import TestCase
from django.test.client import Client
import test_utils.utils.twill_runner as twill
from twill.commands import TwillAssertionError
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO #to make twill quiet

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
from django.utils.http import urlencode

import re

class RPXTest(TestCase):

    def setUp(self):
        twill.setup()
        #Supressing output of twill
        twill.twill.set_output(StringIO())
    def tearDown(self):
        twill.teardown()

    def test_openid_login(self):
        openid_identifier = 'http://unittest.myopenid.com/'
        openid_password = 'unittest'

        OPENID_LOGIN_URL = 'https://django-rpx-test.rpxnow.com/openid/start'
        #RPX wants to send user to POST to this token_url after login. But since
        #we can intercept the token value from the responses, we can craft our own
        #POST to the local app. Therefore, we can just set a dummy token_url.
        args = {
            'token_url':'http://example.com/',
            'openid_identifier': openid_identifier,
            #These two are required by RPX:
            'callback': 'RPXNOW._xdCallbacks[0]',
            'callbackScheme': 'https',
        }
        OPENID_LOGIN_URL += '?' + urlencode(args)
        #print OPENID_LOGIN_URL

        #Visit the login url to be redirected to the OpenID provider's site
        #for login. In our case, we are using myopenid.com.
        twill.go(OPENID_LOGIN_URL)
        #If we are already logged in through myopenid, then RPX will redirect 
        #through the myopenid site back to RPX. So we check that here:
        try:
            twill.url('https://www.myopenid.com/signin_password.+')
            
            #Enter our password and submit the form on the myopenid.com website.
            twill.formvalue(1, 'password', openid_password)
            twill.submit()
        except TwillAssertionError:
            twill.url('https://django-rpx-test.rpxnow.com/openid/finish.+')

        #Pull out the redirect url
        contents = twill.show()
        #The URL is part of javascript in <head>, but it's heavily escaped. We
        #remove all of the '\' characters.
        contents = contents.replace('\\', '')
        m = re.search(r'redirectUrl":"(.+?)"', contents)
        self.assertTrue(type(m.group(1)) is str)
        redirect_url = m.group(1)

        #Visiting the redirect url will result in a page with form with the 
        #token in a hidden input field. If we wait too long, the redirect url
        #expires and we get a blank page.
        twill.go(redirect_url)
        twill.code(200)
        contents = twill.show()
        #Pull out the token value
        soup = BeautifulSoup(contents)
        token = soup.find('input', id = 'token')
        token = token['value']
        #Verify that the token is a hash
        self.assertTrue(len(token) == 40)
        #(OR, we can replace the action URL in our form to point to local.)

        return token

    def test_registration(self):
        #First login and get the token
        token = self.test_openid_login()

        #Now use the token to call our rpx_response url:
        c = Client()
        #Undocumented follow = True option follows the redirect so that response
        #is the response of the redirect page.
        response = c.post('/accounts/rpx_response/', {'token': token}, follow = True)
        #Since this is first time account is logging in, we expect user to register.
        register_url = '/accounts/register/?next=%2Faccounts%2Fprofile%2F'
        self.assertRedirects(response, register_url)
        #Make sure the register.html template is rendered. Since register.html
        #inherits from base.html, response.template is a list of template obj
        #ordered by order in which they were rendered.
        self.assertTrue(response.template[0].name == 'django_rpx_plus/register.html')
        self.failUnlessEqual(response.status_code, 200)

        #Register new user. Note that we don't need to use the 'id_' prefix on
        #form fields.
        response = c.post(register_url, 
                          {'username': 'unittest', 'email': 'unittest@mailinator.com'}, 
                          follow = True)
        profile_url = '/accounts/profile/'
        self.assertRedirects(response, profile_url)
        self.assertTrue(response.template[0].name == 'app/profile.html')
        self.failUnlessEqual(response.status_code, 200)
    
    #def test_logout(self):
    #    c = Client()
    #    response = c.get('/accounts/logout/')
    #    self.assertTrue(response.template[0].name == 'django_rpx_plus/logged_out.html')
    #    self.failUnlessEqual(response.status_code, 200)
    
    def test_login(self):
        #Database is flushed for each test, so we need to register first.
        self.test_registration()

        #Then login again:
        token = self.test_openid_login()

        #Now use the token to call our rpx_response url:
        c = Client()
        #Undocumented follow = True option follows the redirect so that response
        #is the response of the redirect page.
        response = c.post('/accounts/rpx_response/', {'token': token}, follow = True)

        #Since this is not the first time user has logged in, we expect a redirect
        #to the profile page.
        profile_url = '/accounts/profile/'
        self.assertRedirects(response, profile_url)
        self.assertTrue(response.template[0].name == 'app/profile.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_login_required(self):
        login_url = '/accounts/login/'
        #Now make sure we are logged out by trying to grab pages which we are not
        #authorized to view.
        c = Client()
        test_url = '/accounts/profile/'
        response = c.get(test_url, follow = True)
        self.assertRedirects(response, login_url+'?next='+test_url)
        self.assertTrue(response.template[0].name == 'django_rpx_plus/login.html')
        
        test_url = '/accounts/rpx_response/'
        response = c.get(test_url, follow = True)
        #This redirect is different. The redirect, unlike the login_required
        #decorator, also encodes the query params.
        self.assertRedirects(response, login_url+'?next=%2Faccounts%2Fprofile%2F')
        self.assertTrue(response.template[0].name == 'django_rpx_plus/login.html')
        
        test_url = '/accounts/register/'
        response = c.get(test_url, follow = True)
        #This redirect is different. The redirect is to the 'auth_login' page
        #which appends the '/accounts/profile/' next on the end.
        self.assertRedirects(response, login_url+'?next=/accounts/profile/')
        self.assertTrue(response.template[0].name == 'django_rpx_plus/login.html')

        test_url = '/accounts/associate/'
        response = c.get(test_url, follow = True)
        self.assertRedirects(response, login_url+'?next='+test_url)
        self.assertTrue(response.template[0].name == 'django_rpx_plus/login.html')
        
        test_url = '/accounts/associate/delete/1/'
        response = c.get(test_url, follow = True)
        self.assertRedirects(response, login_url+'?next='+test_url)
        self.assertTrue(response.template[0].name == 'django_rpx_plus/login.html')

        test_url = '/accounts/associate/rpx_response/'
        response = c.get(test_url, follow = True)
        #This uses the login_required decorator, which is why it's different than
        #/accounts/rpx_response/.
        self.assertRedirects(response, login_url+'?next='+test_url)
        self.assertTrue(response.template[0].name == 'django_rpx_plus/login.html')

