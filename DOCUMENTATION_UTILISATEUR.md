# Documentation utilisateur - Une faim de vie au Croisic

## Visiteur

- Accède à la page d'accueil et aux articles publiés.
- Consulte les publicités validées.
- Ne peut pas commenter ni proposer de publicité.

## Utilisateur inscrit

### Ajouter un commentaire
1. Se connecter via `/login/`.
2. Ouvrir un article.
3. Cliquer sur **Commenter**.
4. Saisir le message puis valider.
5. Le commentaire est placé en **en attente** de modération.

### Proposer une publicité commerçant
1. Se connecter.
2. Aller sur `/ads/submit/`.
3. Compléter titre, commerçant, image (optionnelle), texte et tarif.
4. Envoyer.
5. La publicité est en **en attente**.

## Animateur

### Publier un article
1. Se connecter avec un compte animateur/admin.
2. Aller sur `/post/create/`.
3. Renseigner les champs principaux.
4. Choisir l'état : brouillon ou publié.

### Ajouter des médias avancés à un article

- Notebook Python : uploader un fichier HTML pré-généré.
- Power BI : coller le code iframe d'embed.
- Vidéo : URL YouTube/Vimeo ou fichier vidéo.

### Modérer les commentaires

1. Ouvrir `/moderation/comments/`.
2. Cliquer sur **Valider** ou **Rejeter**.

### Modérer les publicités

1. Ouvrir `/moderation/ads/`.
2. Cliquer sur **Valider** ou **Rejeter**.

## Administrateur

- Dispose de toutes les permissions via `/admin/`.
- Peut gérer utilisateurs, groupes, contenus et modération.

## Comptes de démonstration (seed)

Après exécution de `python manage.py seed_demo_data` :

- animateur
- lecteur
- commercant

Mot de passe par défaut : `ChangeMe123!` (sauf si redéfini via `--password`).
