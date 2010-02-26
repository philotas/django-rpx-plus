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


INSTALLATION:
-------------

1. Put the code in a directory called 'django_rpx' somewhere in your path
   and put 'django_rpx' in your installed apps.

2. create a url path that serves up the rpx_response view in views.py.

3. You will also need to put the RPXNOW_API_KEY, RPXNOW_REALM and optionally
   RPX_TRUSTED_PROVIDERS into your settings.py (RPXNOW_REALM isn't well
   documented on the rpxnow site, but it's the subdomain of rpxnow.com that
   handles your HTTP callback - e.g. if http://possumpalace-blog.rpx.now is the
   destination of the link in your provided rpxnow snippet, your realm is
   "possumpalace-blog".

4. You will also need to add rpx to your authentication providers list
       AUTHENTICATION_BACKENDS = (
         'rpx.backends.RpxBackend',
         'django.contrib.auth.backends.ModelBackend',
       )
5. You might want to include the rpx template tags in your site code
   somewhere to provide a login link. Their embedded iframe version is not yet
   templated up, but the popup/link-out version is provided.
  

Authors
-------

* Michael Huynh (http://github.com/mikexstudios)
  Rewrote much of django-rpx, adding support for multiple account mapping,
  removing need to use the User.is_active field, and included example app.
* Alex Kessinger (http://github.com/voidfiles)
  Added template snippets, made django-rpx into a module, and added setup.py.
* Dan MacKinlay (http://github.com/howthebodyworks)
  Started django-rpx and wrote most of the functionality in the app. 
* Brian Ellin (RPX Product Manager)
  Provided an [initial recipe][1] for interacting with RPX.

[1] http://appengine-cookbook.appspot.com/recipe/accept-google-aol-yahoo-myspace-facebook-and-openid-logins/    "Initial RPX python recipe"


TODO
----

* Could really use a test suite. Help is welcome with the intricacies of
  mocking out this kind of messy redirect/AJAX service. (automated browser,
  sure, but how do I mock out the rpxnow service itself?)

* Implement sign-in interface customisation and localisation:
  https://rpxnow.com/docs#sign-in_interface

* Optionally implement the mapping api https://rpxnow.com/docs#mappings to
  ease integration?

* See [Issues][2] for more.
