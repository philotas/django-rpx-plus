django-rpx-plus
===============

Purpose
-------

A pluggable django application that enables users to login to your django app
using the RPX, a hosted OpenID service that handles authentication from many
OpenID providers, including Google, Facebook, Twitter, Yahoo, Microsoft Live,
and other OpenID providers.

django-rpx-plus is intended to replace the default/bundled authentication
backend and registration process in django. In other words, unlike django-rpx, 
django-rpx-plus, is not designed to give users the option to register and login
using your site's existing authentication system (typically using a username
and password). Rather, the purpose of django-rpx-plus is to **only** have RPX
style logins throughout your whole site.


What does it do?
----------------

* Let's users login using RPX service.

* If user is new to your site, prompts them to register (provide a username and
  email address).

* Allows users to associate multiple RPX logins with a single User. This is
  **not** the premium RPX mapping feature, but it essentially does the same
  thing without you needing to sign up for a pro account.

* Provides an example app with basic templates to demonstrate how to use 
  django-rpx-plus.


Differences from django-rpx
---------------------------

django-rpx-plus was forked from django-rpx using the work done by Dan MacKinlay
and Alex Kessinger. However, it was postfixed with '-plus' because: 

1. The additional associate feature was added. 

2. We no longer rely on checking for User.is_active to determine the
   registration step. (This greatly simplifies authentication checking since we
   only need to use the @login_required decorator now).

3. The design is intended to replace existing login systems--not work alongside
   the existing systems. That is, django-rpx-plus intends to be the **only* way
   for users to login and register on your site.


Installation
------------

1.  Place the directory 'django_rpx_plus' somewhere in your path. You can do this
    manually or by running:
        python setup.py install
    Ideally, you would be using a virtualenv and install to that env using pip.

    **NOTE**: django_rpx_plus depends on the django messages framework (see the
    [backported messages framework][1] if you are using <= django 1.1.1) and 
    django-picklefield. Using setup.py will automatically install these.
    
2.  Edit settings.py and place `django_rpx_plus` in your `INSTALLED_APPS`.

3.  Also add the following django_rpx_plus settings to your settings.py and fill
    in the values with parameters provided by RPX.
        ############################
        #django_rpx_plus settings: #
        ############################
        RPXNOW_API_KEY = ''
        
        # The realm is the subdomain of rpxnow.com that you signed up under. It handles 
        # your HTTP callback. (eg. http://mysite.rpxnow.com implies that RPXNOW_REALM  is
        # 'mysite'.
        RPXNOW_REALM = ''
        
        # (Optional)
        #RPX_TRUSTED_PROVIDERS = ''

        # (Optional)
        # Sets the language of the sign-in interface for *ONLY* the popup and the embedded
        # widget. For the valid language options, see the 'Sign-In Interface Localization'
        # section of https://rpxnow.com/docs. If not specified, defaults to 'en'.
        #RPX_LANGUAGE_PREFERENCE = 'en'
        
        # If it is the first time a user logs into your site through RPX, we will send 
        # them to a page so that they can register on your site. The purpose is to 
        # let the user choose a username (the one that RPX returns isn't always suitable)
        # and confirm their email address (RPX doesn't always return the user's email).
        REGISTER_URL = '/accounts/register/'

4.  Add `django_rpx_plus.backends.RpxBackend` to your `AUTHENTICATION_BACKENDS`. It
    should come before the default `ModelBackend`.
        # Auth backend config tuple does not appear in settings file by default. So we
        # specify both the RpxBackend and the default ModelBackend:
        AUTHENTICATION_BACKENDS = (
            'django_rpx_plus.backends.RpxBackend', 
            'django.contrib.auth.backends.ModelBackend', #default django auth
        )

5.  Add `django.core.context_processors.request` to your `TEMPLATE_CONTEXT_PROCESSORS`:
        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.auth', #for user template var
            #'django.core.context_processors.debug',
            #'django.core.context_processors.i18n',
            'django.core.context_processors.media', #for MEDIA_URL template var
            'django.core.context_processors.request', #includes request in RequestContext
        )

6.  You also need to make sure the django messages framework is installed correctly.
    See the [installation instructions][2] for more information.

7.  In your app `urls.py`, add to `urlpatterns`:
        (r'^accounts/', include('django_rpx_plus.urls')),

8.  You need to create the relevant template files for django_rpx_plus in your
    app's template directory. For example, if your app is called APP, put the
    django_rpx_plus template files in:
        APP/templates/django_rpx_plus/
    Sample django_rpx_plus template files have been provided in the example app.
    If you create your own templates, note that you can use RPX template tags
    by adding the following to the top of your template file:
        {% load rpx %}


Tips
----

*   The `extra` parameter in the rpx template tags takes a dictionary that will be
    `extra = urlencode(extra)` into a URL GET query string. However, the problem is
    that you can't pass a dictionary as a param in a template tag. So typically,
    `extra` is set in the view function as a template variable. However, this limits
    the your flexibility since if you want to add entries to `extra`, you may need
    to override some of the provided django-rpx-plus views (such as login). If you
    have any ideas on how to improve handling of `extra`, please let me know.


Authors
-------

* [Michael Huynh](http://github.com/mikexstudios)
  Rewrote much of django-rpx, adding support for multiple account mapping,
  removing need to use the User.is_active field, and included example app.

* [Alex Kessinger](http://github.com/voidfiles)
  Added template snippets, made django-rpx into a module, and added setup.py.

* [Dan MacKinlay](http://github.com/howthebodyworks)
  Started django-rpx and wrote most of the functionality in the app. 

* Brian Ellin (RPX Product Manager)
  Provided an [initial recipe][3] for interacting with RPX.
  

TODO
----

* Could really use a test suite. Help is welcome with the intricacies of
  mocking out this kind of messy redirect/AJAX service. (automated browser,
  sure, but how do I mock out the rpxnow service itself?)

* Implement sign-in interface customisation and localisation:
  https://rpxnow.com/docs#sign-in_interface

* Optionally implement the mapping api https://rpxnow.com/docs#mappings to
  ease integration?

* See [Issues][4] for more.



[1]: http://github.com/mikexstudios/django-messages-framework "Backported django messages framework"
[2]: http://docs.djangoproject.com/en/dev/topics/auth/#installation "Django messages framework installation"
[3]: http://appengine-cookbook.appspot.com/recipe/accept-google-aol-yahoo-myspace-facebook-and-openid-logins/    "Initial RPX python recipe"
[4]: http://github.com/mikexstudios/django-rpx-plus/issues    "Issues"
