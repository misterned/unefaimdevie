# Une faim de vie au Croisic

Application Django de journal/webzine culturel local pour les habitants du Croisic.

## 1) Fonctionnalités couvertes

- Publication d'articles par animateur/admin
- Commentaires visiteurs avec modération
- Publicités proposées par les visiteurs avec modération
- Support des contenus enrichis sur les posts :
  - notebook Python (HTML pré-généré)
  - rapport Power BI (embed iframe)
  - vidéo (URL ou upload)

## 2) Stack technique

- Django (architecture classique, sans DRF)
- Templates Django + Bootstrap 5
- SQLite en dev, PostgreSQL en production
- WhiteNoise pour les statiques en production

## 3) Arborescence principale

- `croisicwebzine/` : configuration projet
- `core/` : modèles, vues, formulaires, templates
- `.github/workflows/` : CI/CD
- `deploy/` : scripts OVH/Azure

## 4) Installation locale

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 5) Variables d'environnement

Voir `.env.example`.

- `DJANGO_SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL` (prioritaire) ou variables PostgreSQL `POSTGRES_*`

### Azure Blob (media en production)

Pour stocker les images/fichiers dans Azure Blob Storage, configurez dans App Service:

- `AZURE_STORAGE_ACCOUNT_NAME` (ex: `unefaimdeviemedia`)
- `AZURE_STORAGE_CONTAINER` (ex: `media`)
- `AZURE_STORAGE_CONNECTION_STRING` (connection string complète du Storage Account)
- `USE_AZURE_BLOB_MEDIA=true` (recommandé pour forcer le mode Blob)

Notes:

- `USE_AZURE_BLOB_MEDIA=true` force l'utilisation d'Azure Blob même si vos variables changent plus tard.
- En production sur Azure App Service (`WEBSITE_SITE_NAME` défini et `DEBUG=False`), le projet échoue au démarrage si le Blob n'est pas configuré (comportement volontaire pour éviter les erreurs silencieuses).
- Fournir au moins un mode d'authentification Blob: `AZURE_STORAGE_CONNECTION_STRING` ou `AZURE_STORAGE_ACCOUNT_KEY`.
- Un redémarrage de l'App Service est nécessaire après modification des App Settings.
- Vérification rapide:

```bash
python manage.py shell -c "from django.conf import settings; print(settings.STORAGES['default']['BACKEND']); print(settings.MEDIA_URL)"
```

Le backend attendu est `storages.backends.azure_storage.AzureStorage`.

## 6) Gestion des rôles

### Visiteur
- lecture des articles et publicités validées
- dépôt de commentaires soumis à modération
- soumission de publicités soumises à modération

### Animateur
- créer/modifier des articles
- modérer les commentaires déposés sur ses propres articles
- modérer les publicités

### Admin
- tous les droits Django et modération globale

Les comptes animateurs sont créés par l'administration. Il n'existe pas d'inscription publique.

> Recommandation : créer un groupe Django `animateur` et y ajouter les comptes animateurs.

## 7) URLs principales

- `/` : accueil
- `/posts/` : liste des posts
- `/post/<id>/` : détail d'un post
- `/post/create/` : création post (animateur/admin)
- `/post/<id>/edit/` : modification post (animateur/admin)
- `/post/<id>/comment/` : commentaire visiteur
- `/moderation/comments/` : modération commentaires des articles de l'animateur
- `/ads/` : publicités validées
- `/ads/submit/` : soumission publicité
- `/moderation/ads/` : modération publicités
- `/espace-animateur/connexion/`, `/logout/`

## 8) Déploiement

### Azure App Service

- Workflow `.github/workflows/deploy-azure.yml`
- Script startup : `deploy/azure/startup.sh`
- Secrets requis :
  - `AZURE_WEBAPP_NAME`
  - `AZURE_WEBAPP_PUBLISH_PROFILE`

### OVH mutualisé

- Script rsync : `deploy/ovh/deploy_ovh.sh`
- Entrée WSGI : `deploy/ovh/passenger_wsgi.py`
- Workflow manuel : `.github/workflows/deploy-ovh.yml`
- Secrets requis :
  - `OVH_SSH_KEY`, `OVH_HOST`, `OVH_USER`, `OVH_PATH`

## 9) CI/CD

- `ci.yml` : check Django + migrations + tests
- `deploy-azure.yml` : déploiement Azure
- `deploy-ovh.yml` : déploiement OVH manuel

## 10) Commandes utiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py test
python manage.py seed_demo_data
python manage.py seed_demo_data --password "MonMotDePasseFort!"
```

## 11) Seed de démonstration (fixture + commande)

Le projet inclut :

- une fixture JSON : `core/fixtures/demo_seed.json`
- une commande idempotente : `python manage.py seed_demo_data`

La commande :

- crée le groupe `animateur`
- crée/actualise le compte `animateur`
- charge les posts/publicités de démonstration depuis la fixture
- crée des commentaires approuvés + en attente

Mot de passe par défaut : `ChangeMe123!` (modifiable avec `--password`).
