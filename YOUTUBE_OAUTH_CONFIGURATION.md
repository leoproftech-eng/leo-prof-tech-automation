# Connexion de Léo & le Prof à YouTube — sécurité et validation

**État : préparé, mais pas encore autorisé.** GitHub est connecté ; YouTube n'a pas encore accordé de droit de téléversement au workflow. **Le workflow quotidien ne publie rien.**

## Pourquoi une étape Google est indispensable
YouTube Data API exige un consentement OAuth du propriétaire de la chaîne. Un simple lien public vers la chaîne ou une connexion GitHub ne donne pas le droit de publier.

Chaîne cible : `UCk-B48dgzUSkcWsQxAQboQw` — https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw

## Configuration sans installation sur PC

1. Ouvrir https://console.cloud.google.com/ avec **le compte qui gère la chaîne**. Créer un projet Google Cloud dédié, par exemple `Leo-et-le-Prof`, ou sélectionner un projet existant que vous contrôlez.
2. Ouvrir **APIs & Services → Library** et activer **YouTube Data API v3**.
3. Dans **Google Auth Platform → Branding / Audience / Data Access**, configurer l'écran de consentement OAuth (les intitulés peuvent varier). Ajouter le compte Google autorisé aux utilisateurs de test si nécessaire.
4. Créer un identifiant OAuth **Application Web**. Autoriser exactement le redirect URI : `https://developers.google.com/oauthplayground`. Garder l'identifiant client et son secret privés.
5. Ouvrir https://developers.google.com/oauthplayground/ ; cliquer sur l'icône engrenage et activer **Use your own OAuth credentials**, puis renseigner les identifiants de **votre** projet (pas dans GitHub ni dans ce chat).
6. Autoriser les deux scopes :
   - `https://www.googleapis.com/auth/youtube.upload`
   - `https://www.googleapis.com/auth/youtube.readonly`
   Cliquer sur **Authorize APIs**, choisir le compte propriétaire de **Léo & le Prof**, vérifier les permissions puis accepter.
7. **Exchange authorization code for tokens** et récupérer le **refresh token**. Si aucun refresh token n'est émis, retirer l'autorisation antérieure de l'application et refaire la procédure en demandant l'accès hors ligne. Ne jamais partager ce jeton dans un message, une capture ou un dépôt.
8. Aller dans les paramètres GitHub du dépôt `leoproftech-eng/leo-prof-tech-automation` → **Settings → Secrets and variables → Actions → New repository secret**. Créer les secrets suivants, avec les valeurs obtenues :
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`
9. Exécuter manuellement https://github.com/leoproftech-eng/leo-prof-tech-automation/actions/workflows/youtube-private-test.yml et regarder si une **vidéo privée** apparaît sur la bonne chaîne. Ce test ne crée aucune publication publique.

## Important : durée de validité des jetons

Pour un projet OAuth configuré en **Testing** avec type d'audience externe, les refresh tokens expirent généralement après **7 jours** pour des permissions YouTube. Ce mode convient à un essai, pas à une automatisation durable. Il faudra examiner les conditions de publication de l'application OAuth et les règles de Google avant activation à long terme.

## Sécurité du test

- Le code vérifie que la chaîne autorisée correspond à l'ID cible.
- Le téléversement s'effectue **en privé uniquement** (`privacyStatus=private`).
- Le workflow de génération quotidienne reste indépendant du téléversement.
- Aucune donnée secrète n'est présente dans le dépôt.
- La publication publique ne doit être activée qu'après réussite du test privé et un nouveau contrôle qualité.
- Les projets API non vérifiés peuvent être soumis à des restrictions supplémentaires.

## Références officielles
- https://developers.google.com/youtube/data/guides/authentication
- https://developers.google.com/youtube/data/guides/uploading_a_video
- https://developers.google.com/identity/protocols/oauth2
