# Documentation utilisateur - Une faim de vie au Croisic

## Visiteur

- Accède à la page d'accueil et aux articles publiés.
- Consulte les publicités validées.
- Peut déposer un commentaire sans créer de compte.
- Peut proposer une publicité sans créer de compte.

### Ajouter un commentaire
1. Ouvrir un article.
2. Cliquer sur **Commenter**.
3. Renseigner son nom, éventuellement son email, puis le message.
4. Valider.
5. Le commentaire est placé en **en attente** de modération.

### Proposer une publicité commerçant
1. Aller sur `/ads/submit/`.
2. Compléter titre, commerçant, image (optionnelle), texte et tarif.
3. Envoyer.
4. La publicité est en **en attente**.

## Animateur

### Accéder à l'espace animateur
1. Utiliser l'URL de connexion transmise par l'administration : `/espace-animateur/connexion/`.
2. Se connecter avec un compte animateur/admin.

### Publier un article
1. Se connecter avec un compte animateur/admin.
2. Aller sur `/post/create/`.
3. Renseigner les champs principaux.
4. Choisir l'état : brouillon ou publié.

### Modifier un article
1. Ouvrir l'article concerné.
2. Cliquer sur **Modifier l'article**.
3. Les animateurs ne modèrent que les commentaires de leurs propres articles.

### Ajouter des médias avancés à un article

- Notebook Python : uploader un fichier HTML pré-généré.
- Power BI : coller le code iframe d'embed.
- Vidéo : URL YouTube/Vimeo ou fichier vidéo.

### Modérer les commentaires

1. Ouvrir `/moderation/comments/`.
2. Seuls les commentaires des articles de l'animateur sont affichés.
3. Cliquer sur **Valider** ou **Rejeter**.

### Modérer les publicités

1. Ouvrir `/moderation/ads/`.
2. Cliquer sur **Valider** ou **Rejeter**.

## Administrateur

- Dispose de toutes les permissions via `/admin/`.
- Peut gérer utilisateurs, groupes, contenus et modération globale.

## Compte de démonstration (seed)

Après exécution de `python manage.py seed_demo_data` :

- animateur

Mot de passe par défaut : `ChangeMe123!` (sauf si redéfini via `--password`).
