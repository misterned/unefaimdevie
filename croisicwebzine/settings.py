# croisicwebzine/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_str(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _env_bool(name: str, default: bool = False) -> bool:
    value = _env_str(name, "1" if default else "0").lower()
    return value in {"1", "true", "yes", "on"}

SECRET_KEY = _env_str("DJANGO_SECRET_KEY", "dev-secret-key")

DEBUG = _env_bool("DEBUG", True)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".azurewebsites.net",
]

extra_hosts = _env_str("ALLOWED_HOSTS", "")
if extra_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in extra_hosts.split(",") if h.strip()])

azure_account_name = _env_str("AZURE_STORAGE_ACCOUNT_NAME")
azure_container = _env_str("AZURE_STORAGE_CONTAINER")
azure_custom_domain = _env_str("AZURE_STORAGE_CUSTOM_DOMAIN")

# Legacy aliases kept for compatibility with older app settings naming.
if not azure_account_name:
    azure_account_name = _env_str("AZURE_ACCOUNT_NAME")
if not azure_container:
    azure_container = _env_str("AZURE_CONTAINER")

azure_media_enabled = _env_bool("USE_AZURE_BLOB_MEDIA", False) or bool(
    azure_account_name and azure_container
)

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

if azure_media_enabled:
    INSTALLED_APPS.append("storages")

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
LOGIN_URL = '/espace-animateur/connexion/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------------------------------------
# FICHIERS STATIQUES ET MEDIAS
# -------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

if azure_media_enabled:

    STORAGES["default"] = {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": azure_account_name,
            "account_key": _env_str("AZURE_STORAGE_ACCOUNT_KEY"),
            "connection_string": _env_str("AZURE_STORAGE_CONNECTION_STRING"),
            "azure_container": azure_container,
            "custom_domain": azure_custom_domain,
            "overwrite_files": False,
        },
    }

    if azure_custom_domain:
        MEDIA_URL = f"https://{azure_custom_domain}/"
    else:
        MEDIA_URL = f"https://{azure_account_name}.blob.core.windows.net/{azure_container}/"

    # Not used by Azure backend, but kept for compatibility with code expecting MEDIA_ROOT.
    MEDIA_ROOT = BASE_DIR / "media"
else:
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": str(BASE_DIR / "media"),
            "base_url": "/media/",
        },
    }
    MEDIA_URL = '/media/'
    default_media_root = BASE_DIR / "media"
    if not DEBUG and _env_str("WEBSITE_SITE_NAME"):
        # Azure App Service persistent writable path.
        default_media_root = Path("/home/site/wwwroot/media")
    MEDIA_ROOT = Path(_env_str("MEDIA_ROOT", str(default_media_root)))

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in _env_str("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", False)
CSRF_COOKIE_SECURE = _env_bool("CSRF_COOKIE_SECURE", False)

# -------------------------------------------------------------
# CONFIGURATION EMAIL (pour notifications/modération)
# -------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'