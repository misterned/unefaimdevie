# croisicwebzine/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".azurewebsites.net",
    os.environ.get("RENDER_EXTERNAL_HOSTNAME", ""),
]

extra_hosts = os.environ.get("ALLOWED_HOSTS", "")
if extra_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in extra_hosts.split(",") if h.strip()])

# -------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App principale
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise pour servir les statiques en production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'croisicwebzine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", BASE_DIR / "core" / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.role_flags',
            ],
        },
    },
]

WSGI_APPLICATION = 'croisicwebzine.wsgi.application'

# -------------------------------------------------------------
# BASE DE DONNÉES (PostgreSQL en production)
# -------------------------------------------------------------

if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            os.environ.get("DATABASE_URL"), conn_max_age=600
        )
    }
elif os.environ.get("POSTGRES_DB"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("POSTGRES_DB", "croisic"),
            'USER': os.environ.get("POSTGRES_USER", "postgres"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "postgres"),
            'HOST': os.environ.get("POSTGRES_HOST", "localhost"),
            'PORT': os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------
# AUTHENTIFICATION
# -------------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------------------------------------
# FICHIERS STATIQUES ET MEDIAS
# -------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False") == "True"

# -------------------------------------------------------------
# CONFIGURATION EMAIL (pour notifications/modération)
# -------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'