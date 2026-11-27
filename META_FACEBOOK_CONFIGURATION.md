# Meta → GitHub : autorisation unique de la Page « Léo & le Prof »

## Objectif
Publier chaque Short créé dans `studio_officiel_statique.py` sur YouTube **et** Facebook Reels, depuis le même fichier MP4, sans import manuel quotidien.

## Ce qui est fait
- `facebook_reels_publish.py` : upload officiel en 3 phases START / rupload / FINISH, confirmation de l'identité de la Page, anti-doublon par référence d'épisode (échec conservateur si la lecture des Reels est impossible).
- `.github/workflows/daily-generate.yml` : le job quotidien réutilise le fichier MP4 après génération et lancement YouTube.
- En absence d'autorisation Meta, la partie Facebook indique « non connecté » et **ne publie pas**. Ne jamais coller des tokens dans un chat ou un fichier Git suivi.

## Étape d'autorisation Meta (une seule configuration initiale)
1. Ouvrir https://developers.facebook.com/apps/ avec un compte Facebook disposant du contrôle total sur la Page « Léo & le Prof ».
2. Créer une application Meta appropriée à la gestion et publication de Pages. Ajouter le cas d'utilisation Facebook Login / Pages API si disponible.
3. Demander/autoriser selon les possibilités de Meta : `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`. Pour toute autre permission imposée par l'API, consulter les exigences Meta en vigueur ; le mode développement, l'éligibilité et la revue d'application peuvent limiter la publication.
4. Obtenir **l'identifiant numérique de la Page** et son **Page access token**, avec les permissions requises. Pour une automatisation durable, s'assurer qu'il est à longue durée de vie, que les rôles du compte sont corrects et prévoir la rotation/révocation. Ne jamais publier les tokens.
5. Dans GitHub : https://github.com/leoproftech-eng/leo-prof-tech-automation/settings/secrets/actions créer :
   - `META_PAGE_ID` : identifiant numérique de la Page « Léo & le Prof ».
   - `META_PAGE_ACCESS_TOKEN` : jeton d'accès de la Page délivré par Meta.
6. Vérifier un épisode en privé / lancement contrôlé après connexion, avant d'exiger des publications quotidiennes sans supervision.

## Limites à surveiller
- La publication Meta n'est pas activée tant que les deux secrets ne sont pas présents et validés.
- Aucune confirmation de publication réelle Facebook au moment de cette configuration.
- Le workflow quotidien ne dispose que de **12 questions (4 Shorts)** : le pilote + trois jours. Les épisodes ne se répètent pas ; la publication s'arrête quand la banque est épuisée. Ajouter une source durable et vérifiée de nouvelles questions, avec contrôle de qualité et correction des faits, avant de promettre une publication perpétuelle.
- Les tâches cron GitHub peuvent démarrer en retard ou être ignorées. L'heure de **18 h America/Toronto** est la cible, non une garantie à la minute.
- Le consentement Google OAuth en mode « Testing » peut rendre son refresh token invalide en environ 7 jours ; régler l'état de publication de l'application Google séparément.
- L'accès Meta et les autorisations Page peuvent expirer ou être révoqués. Prévoir un contrôle d'échec avec alertes et procédure de renouvellement.
- Ne pas mettre les accès aux comptes ou les valeurs secrètes dans un fichier GitHub public, capture d'écran ou conversation.

## Sources officielles
- https://developers.facebook.com/docs/graph-api/reference/page/video_reels
- https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
