from auctions.settings import *

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auctions',
        'USER': 'root',
        'PASSWORD': 'qweqwe',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dmitrysulin@gmail.com'
EMAIL_HOST_PASSWORD = 'Acetonio26'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
