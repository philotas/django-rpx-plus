# Django settings for example project.

# There might be a better way to determine messages framework without actually
# importing it. Maybe check django.VERSION? (but that wouldn't work well for
# trunk, I think)
BUILT_IN_MESSAGES_FRAMEWORK = False
try:
    import django.contrib.messages.context_processors.messages
    BUILT_IN_MESSAGES_FRAMEWORK = True
except ImportError:
    pass

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'django_rpx_example'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')q+la(53wx8v(=j*+jzb-k#z6i%7%0khuz_+dj_*yo=--x7q#_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
if BUILT_IN_MESSAGES_FRAMEWORK:
    MIDDLEWARE_CLASSES.append('django.contrib.messages.middleware.MessageMiddleware')
else:
    MIDDLEWARE_CLASSES.append('django_messages_framework.middleware.MessageMiddleware')

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'app', #This is our app. Ideally, this would be named better.
    'django_rpx', #Put this after our app with template overrides.
]
if BUILT_IN_MESSAGES_FRAMEWORK:
    INSTALLED_APPS.append('django.contrib.messages')
else:
    INSTALLED_APPS.append('django_messages_framework')

# Template context processors do not appear in settings file by default. But we
# require the request context_processor and the message framework also has a
# context processor. So both are added here:
TEMPLATE_CONTEXT_PROCESSORS = [
    #'django.core.context_processors.auth',
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    #'django.core.context_processors.media',
    'django.core.context_processors.request', #includes request in RequestContext
    #'django_messages_framework.context_processors.messages', #backport of dev
]
if BUILT_IN_MESSAGES_FRAMEWORK:
    TEMPLATE_CONTEXT_PROCESSORS.append('django.contrib.messages.context_processors.messages')
else:
    TEMPLATE_CONTEXT_PROCESSORS.append('django_messages_framework.context_processors.messages')

# Auth backend config tuple does not appear in settings file by default. So we
# specify both the RpxBackend and the default ModelBackend:
AUTHENTICATION_BACKENDS = (
    'django_rpx.backends.RpxBackend', 
    'django.contrib.auth.backends.ModelBackend', #default django auth
)

# Here are some settings related to auth urls. django has default values for them
# as specified on page: http://docs.djangoproject.com/en/dev/ref/settings/. You
# can override them if you like.
#account.
LOGIN_REDIRECT_URL = '' #default: '/accounts/profile/'
LOGIN_URL = '' #default: '/accounts/login/'
LOGOUT_URL = '' #default: '/accounts/logout/'

########################################
# django messages framework settings:  #
########################################

#First uses CookieStorage for all messages, falling back to using
#SessionStorage for the messages that could not fit in a single cookie.
if BUILT_IN_MESSAGES_FRAMEWORK:
    MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
else:
    MESSAGE_STORAGE = 'django_messages_framework.storage.fallback.FallbackStorage'

#######################
#django_rpx settings: #
#######################
RPXNOW_API_KEY = '920a779d73ab00b6976f652a4fd8d13883f2fdb0'

# The realm is the subdomain of rpxnow.com that you signed up under. It handles 
# your HTTP callback. (eg. http://mysite.rpxnow.com implies that RPXNOW_REALM  is
# 'mysite'.
RPXNOW_REALM = 'suppletext'

# (Optional)
#RPX_TRUSTED_PROVIDERS = ''

# If it is the first time a user logs into your site through RPX, we will send 
# them to a page so that they can register on your site. The purpose is to 
# let the user choose a username (the one that RPX returns isn't always suitable)
# and confirm their email address (RPX doesn't always return the user's email).
REGISTER_URL = '/accounts/register/'


#Import any local settings (eg. production environment) that will override
#these development environment settings. For instance, we will use this to
#keep sensitize database login information from being checked into repo.
try:
    from local_settings import *
except ImportError:
    pass 
