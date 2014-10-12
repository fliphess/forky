import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Executor
REMOTE_EXECUTOR = os.path.join(BASE_DIR, 'remote_executor.py')

# LOGGING
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)-7s %(message)s"
LOG_PREFIX = 'Django Bot'
LOG_FILE = '/tmp/some_log_file.log'
LOG_EXCEPTIONS = '/tmp/exceptions.log'
LOG_VERBOSITY = 3


# LOGIN
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/start'


# LANGUAGE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


DEBUG = True
DEVELOPMENT = False
ALLOWED_HOSTS = []
SECRET_KEY = '5rgj4(l8a*v@gb_g4ilg!7)!dpkv%0uj7ldsav+zi62n9(o5rs'

ROOT_URLCONF = 'control.urls'
WSGI_APPLICATION = 'control.wsgi.application'


# STATIC
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# TEMPLATES
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)


# APPS
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ircbot',
)

# MIDDLEWARE
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# BOT SETTINGS
BOT_NICK = 'FlipperBot'
BOT_IDENT = 'botje'
BOT_NAME = 'Flipjes irc bot: https://github.com/fliphess/forky'
BOT_PREFIX = '\.'
BOT_RECONNECT_DELAY = 20
BOT_EXIT_ON_ERROR = False

# IRC SERVER
IRC_SERVER_HOST = 'irc.xs4all.nl'
IRC_SERVER_PORT = 6667
IRC_SERVER_PASSWORD = None
IRC_SERVER_TIMEOUT = 120

IRC_SERVER_SSL = False
IRC_SERVER_VERIFY_SSL = False
IRC_SERVER_SASL = False

