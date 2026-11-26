# Léo & le Prof Tech

**Chaîne YouTube :** https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw

## Mission
Créer un YouTube Short éducatif par jour en français, avec deux avatars noirs récurrents côte à côte : Léo pose **trois questions technologiques successives**, le Prof répond à chacune simplement et avec rigueur.

## Objectif de production
- **1 seul Short par jour contenant 3 questions et 3 réponses**, publication à 18 h, fuseau `America/Toronto`.
- Niveau : débutant, intermédiaire et expert.
- Domaines : informatique, IA, réseaux, cloud, sécurité, programmation et innovations.
- Format : vertical 9:16 ; durée cible 45 à 90 secondes selon le rythme et la clarté des réponses. Léo à gauche et le Prof à droite, visibles ensemble.
- Aucune installation sur le PC de l'utilisateur.
- Budget cible : 0 $ CA/mois, sous réserve des quotas cloud.

## Architecture envisagée
GitHub Actions → sélection de 3 questions différentes vérifiées → création de 3 échanges question/réponse → synthèse vocale → affichage simultané de Léo (gauche) et du Prof (droite) → montage et sous-titres en un seul Short → contrôle qualité → téléversement via YouTube Data API → publication à 18 h.

## État
- [x] Chaîne YouTube créée
- [x] Logo et bannière préparés
- [x] Dépôt GitHub connecté
- [ ] Moteur de génération des vidéos développé
- [ ] Avatars 2D animables finalisés
- [ ] Premier Short pilote testé
- [ ] Autorisations YouTube OAuth mises en place
- [ ] Workflow quotidien activé

## Sécurité et qualité
Ne jamais ajouter de mot de passe, de jeton OAuth ni de clé API dans ce dépôt public. Conserver les secrets uniquement dans GitHub Actions Secrets. Ne publier que les vidéos passées par des contrôles automatiques; en cas de doute factuel, utiliser un sujet prévalidé.

> Ce dépôt est en préparation : aucune publication automatique n'est encore active.

## Spécification validée du format
- Une seule publication quotidienne, jamais trois Shorts distincts.
- Une vidéo = trois séquences : question 1/réponse 1 ; question 2/réponse 2 ; question 3/réponse 3.
- Deux avatars noirs côte à côte pendant toute la vidéo ; mise en évidence de celui qui parle.
- Conserver les voix françaises jugées satisfaisantes ; améliorer l'animation, la synchronisation et le montage.
- La version Studio V2 actuelle est un prototype à une seule question : **elle doit être adaptée et testée avant toute mise en ligne.**
