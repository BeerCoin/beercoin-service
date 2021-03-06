# Django settings for beercoin project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    ('Ben', 'ben.kampmann+beercoin@gmail.com'),
)

DEFAULT_FROM_EMAIL = "Beercoin <no-reply@beercoin.me>"

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = ''
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static/"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

USERENA_MUGSHOT_DEFAULT = "http://beercoin.me/static/img/default_monster.jpg"
USERENA_SIGNIN_AFTER_SIGNUP = True
USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_REDIRECT_URL = "/#"


# Make this unique, and don't share it with anybody.
SECRET_KEY = '990g168dm9=wve#894v-grfy+whmw!p$$6u2s2%#eya-5i%qj3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1
ROOT_URLCONF = 'beercoin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'beercoin.wsgi.application'

#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

AUTH_PROFILE_MODULE = "util.UserProfile"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userena',
    'guardian',
    'easy_thumbnails',
    'actstream',
    'south',
    'beercoin.beercoin',
    'beercoin.util',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

)

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "in.mailjet.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'sites.site', 'comments.comment'),
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}


PUSHER_APP_ID = os.environ.get("PUSHER_APP_ID")
PUSHER_APP_KEY = os.environ.get("PUSHER_APP_KEY")
PUSHER_APP_SECRET = os.environ.get("PUSHER_APP_SECRET")

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#
# Check for a custom settings_local.py for override values on local system
#
if os.path.exists(os.path.join(BASE_DIR, 'settings_local.py')):
    execfile(os.path.join(BASE_DIR, 'settings_local.py'))
elif os.path.exists(os.path.join(BASE_DIR, 'settings_production.py')):
    execfile(os.path.join(BASE_DIR, 'settings_production.py'))
else:
#
# Required values for Heroku production environment
#
    import sys
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console':{
                'level':'INFO',
                'class':'logging.StreamHandler',
                'stream': sys.stdout
            },
        }
    }
    # Parse database configuration from $DATABASE_URL
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    # Required or get_host will fail on heroku
    ALLOWED_HOSTS = ['www.beercoin.me', 'beercoin.me', 'beercoin.herokuapp.com']

#
# End production settings
#
