# Léo & le Prof Tech

**Chaîne YouTube :** https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw

## Mission
Créer des YouTube Shorts éducatifs en français, avec deux avatars noirs récurrents : Léo pose **une question technologique** et le Prof répond simplement, avec rigueur.

## Objectif de production
- 1 vidéo par jour, publication à 18 h, fuseau `America/Toronto`.
- Niveau : débutant, intermédiaire et expert.
- Domaines : informatique, IA, réseaux, cloud, sécurité, programmation et innovations.
- Format : vertical 9:16, 30 à 60 secondes.
- Aucune installation sur le PC de l'utilisateur.
- Budget cible : 0 $ CA/mois, sous réserve des quotas cloud.

## Architecture envisagée
GitHub Actions → banque de questions vérifiées → génération d'un dialogue → synthèse vocale → animation 2D des deux personnages → montage et sous-titres → contrôle qualité → téléversement via YouTube Data API → publication à 18 h.

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
