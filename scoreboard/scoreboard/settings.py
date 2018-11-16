"""
Django settings for scoreboard project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
import random
import string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'challenges',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'scoreboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'scoreboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'postgres',
         'USER': 'postgres',
         'HOST': 'database',
         'PORT': 5432,
         'CONN_MAX_AGE': None,
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Cookies expire after roughly 10 years.
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 * 10

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Log to a file.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


class SecretKeyManager:
    """ Manage Django's SECRET_KEY on the filesystem.
    """

    # The filesystem path to the secret key
    SECRET_KEY_PATH = '/secrets/django_secret_key.txt'

    # The number of bytes to use for a secret key
    SECRET_KEY_LENGTH = 64

    def __init__(self, path=SECRET_KEY_PATH, key_byte_length=SECRET_KEY_LENGTH):
        """ Write a secret key if one doesn't exist, then read it.
        """
        self.path = path
        self.length = key_byte_length
        # Create the secret key if it does not exist.
        if not os.path.exists(self.path):
            self.write_random_secret_key()
        self.key = self.read_secret_key()

    def write_random_secret_key(self):
        """ Write a random secret key to a file.
        """
        rand_gen = random.SystemRandom()
        choices = string.digits + string.ascii_letters + string.punctuation
        data = [rand_gen.choice(choices) for _ in range(self.length)]
        output = ''.join(data)
        with open(self.path, 'w') as fp:
            fp.write(output)

    def read_secret_key(self):
        """ Read the secret key from a file.
        """
        with open(self.path) as fp:
            return fp.read()


# Read the Django secret key from the filesystem.
SECRET_KEY = SecretKeyManager().key

