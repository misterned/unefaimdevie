# Une faim de vie au Croisic

Application Django de journal/webzine culturel local pour les habitants du Croisic.

## 1) Fonctionnalités couvertes

- Publication d'articles par animateur/admin
- Commentaires utilisateurs avec modération
- Publicités commerçants payantes avec modération
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

## 6) Gestion des rôles

### Visiteur
- lecture seule des articles et publicités validées

### Utilisateur authentifié
- commenter les articles
- soumettre des publicités

### Animateur
- créer/modifier des articles
- modérer commentaires et publicités

### Admin
- tous les droits Django

> Recommandation : créer un groupe Django `animateur` et y ajouter les comptes animateurs.

## 7) URLs principales

- `/` : accueil
- `/posts/` : liste des posts
- `/post/<id>/` : détail d'un post
- `/post/create/` : création post (animateur/admin)
- `/post/<id>/edit/` : modification post (animateur/admin)
- `/post/<id>/comment/` : commentaire utilisateur connecté
- `/moderation/comments/` : modération commentaires
- `/ads/` : publicités validées
- `/ads/submit/` : soumission publicité
- `/moderation/ads/` : modération publicités
- `/login/`, `/logout/`

## 8) Déploiement

### Render

- Fichier `render.yaml` inclus
- Build: installation deps, collectstatic, migrate
- Start: gunicorn
- Déploiement auto possible via hook GitHub Action (`deploy-render.yml`)

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
- `deploy-render.yml` : déclenchement Render via deploy hook
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
- crée/actualise les comptes `animateur`, `lecteur`, `commercant`
- charge les posts/publicités de démonstration depuis la fixture
- crée des commentaires approuvés + en attente

Mot de passe par défaut : `ChangeMe123!` (modifiable avec `--password`).
