from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'postgres',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CORS_ALLOW_CREDENTIALS=True
CORS_ALLOWED_ORIGINS = [
"http://localhost:4200",

]

CSRF_COOKIE_SAMESITE ='None'
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True  # Necesario para SameSite=None, requiere HTTPS


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'