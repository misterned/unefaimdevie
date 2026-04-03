import os
import sys

PROJECT_PATH = os.path.dirname(__file__)
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "croisicwebzine.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
