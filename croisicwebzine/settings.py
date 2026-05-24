# -------------------------------------------------------------
# LOGGING DJANGO POUR AZURE/DEBUG
# -------------------------------------------------------------
import os as _os

_log_handlers = ['console']
_log_extra: dict = {}

# Sur Azure App Service, /home/LogFiles/ est persistant et lisible via Kudu.
# On écrit aussi dans un fichier pour pouvoir le télécharger facilement.
if _os.path.isdir('/home/LogFiles'):
    _log_handlers.append('file')
    _log_extra = {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/home/LogFiles/django.log',
            'encoding': 'utf-8',
        },
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        **_log_extra,
    },
    'root': {
        'handlers': _log_handlers,
        'level': 'INFO',
    },
}
# croisicwebzine/settings.py

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

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
    "unefaimdevie.fr",
    "www.unefaimdevie.fr",
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

is_azure_app_service = bool(_env_str("WEBSITE_SITE_NAME"))

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
    'django.contrib.sitemaps',

    # App principale
    'core',
]

if azure_media_enabled:
    INSTALLED_APPS.append("storages")

APPLICATIONINSIGHTS_CONNECTION_STRING = _env_str("APPLICATIONINSIGHTS_CONNECTION_STRING")

MIDDLEWARE = [
    # Doit être EN PREMIER pour intercepter la sonde Azure avant ALLOWED_HOSTS
    'core.middleware.AzureHealthCheckMiddleware',

    'django.middleware.security.SecurityMiddleware',

    # Whitenoise pour servir les statiques en production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # Mesure du temps de réponse des médias
    'core.middleware.MediaTimingMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Désactivé : Application Insights Azure (provoquait un crash si le module n'est pas installé)
# if APPLICATIONINSIGHTS_CONNECTION_STRING:
#     try:
#         from azure.monitor.opentelemetry import configure_azure_monitor
#         configure_azure_monitor(
#             connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING,
#         )
#     except ImportError:
#         import logging as _log
#         _log.warning(
#             '[settings] azure-monitor-opentelemetry non disponible – '
#             'Application Insights désactivé pour ce démarrage.'
#         )

ROOT_URLCONF = 'croisicwebzine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Prioritize app templates to avoid stale overrides from legacy root templates.
        'DIRS': [BASE_DIR / "core" / "templates", BASE_DIR / "templates"],
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
    sqlite_path = BASE_DIR / 'db.sqlite3'
    if _env_str("WEBSITE_SITE_NAME") and not DEBUG:
        # Azure App Service: keep SQLite on persistent storage, not on temp extracted path.
        sqlite_path = Path("/home/site/wwwroot/db.sqlite3")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_path,
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
    if is_azure_app_service and not DEBUG:
        raise ImproperlyConfigured(
            "Azure App Service production requires Azure Blob media storage. "
            "Set USE_AZURE_BLOB_MEDIA=true and configure AZURE_STORAGE_ACCOUNT_NAME, "
            "AZURE_STORAGE_CONTAINER, and AZURE_STORAGE_CONNECTION_STRING (or account key)."
        )

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

if azure_media_enabled:
    azure_connection_string = _env_str("AZURE_STORAGE_CONNECTION_STRING")
    azure_account_key = _env_str("AZURE_STORAGE_ACCOUNT_KEY")
    if not azure_connection_string and not azure_account_key:
        raise ImproperlyConfigured(
            "Azure Blob storage enabled but no credentials found. "
            "Set AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_KEY."
        )

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

# --- CONFIGURATION SMTP POUR ENVOI REEL ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mail.yahoo.com"  # À adapter selon votre fournisseur
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "nedelec.stephane@yahoo.fr"  # À personnaliser
EMAIL_HOST_PASSWORD = _env_str("EMAIL_HOST_PASSWORD")

# Email expéditeur par défaut (à personnaliser)
DEFAULT_FROM_EMAIL = "Webzine Une faim de vie <noreply@unefaimdevie.fr>"

# URL du site (pour les liens dans les emails)
SITE_URL = "https://unefaimdevie.fr"

# Exemple de configuration SMTP pour envoi réel (décommentez et adaptez si besoin)
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "votre@email.fr"
# EMAIL_HOST_PASSWORD = "votre-mot-de-passe-app"