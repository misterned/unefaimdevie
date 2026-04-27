"""
Point d'entrée WSGI pour le déploiement du projet Django.
"""
import os

from django.core.wsgi import get_wsgi_application
"""
Script de gestion principal pour les commandes Django (manage.py).
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "croisicwebzine.settings")

application = get_wsgi_application()
