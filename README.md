# Léo & le Prof Tech

**Chaîne YouTube :** https://www.youtube.com/channel/UCk-B48dgzUSkcWsQxAQboQw

## Mission
Créer un YouTube Short éducatif par jour en français, avec deux avatars noirs récurrents côte à côte : Léo pose **trois questions technologiques successives**, le Prof répond à chacune simplement et avec rigueur.

## Objectif de production
- **1 seul Short par jour contenant 3 questions et 3 réponses**, publication à 18 h, fuseau `America/Toronto`.
- Niveau : débutant, intermédiaire et expert.
- Domaines : informatique, IA, réseaux, cloud, sécurité, programmation et innovations.
- Format : vertical 9:16 ; durée cible 45 à 90 secondes selon le rythme et la clarté des réponses. Léo à gauche et le Prof à droite, visibles ensemble, tournés l'un vers l'autre (face à face).
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
- Deux avatars noirs face à face dans le même décor : Léo à gauche regarde vers la droite, le Prof à droite regarde vers la gauche ; mise en évidence de celui qui parle.
- Conserver les voix françaises jugées satisfaisantes ; améliorer l'animation, la synchronisation et le montage.
- La version Studio V2 actuelle est un prototype à une seule question : **elle doit être adaptée et testée avant toute mise en ligne.**

## État de l'intégration SadTalker (26 novembre 2026)
- La vérification de l'accès à l'API d'un Space Hugging Face a réussi (workflow de contrôle uniquement).
- **Aucune vidéo animée par SadTalker n'a encore été rendue**. Une connexion réussie ne valide ni le fonctionnement de l'endpoint de rendu, ni le quota GPU, ni les gestes.
- Le connecteur actuel est expérimental : les arguments de génération doivent être alignés sur l'API effective du Space avant un appel réel.
- La publication YouTube reste inactive. Le test de rendu nécessitera les portraits de Léo et du Prof ainsi que les pistes vocales de Studio V2.

## Pilote 3 questions : version 2D (26 novembre 2026)
- Nouveau moteur `pilot_3_questions.py` : 3 questions distinctes, 6 scènes et 2 personnages visibles ensemble.
- Les voix sont synthétisées avec `edge-tts` (Léo : EloiseNeural ; Prof : HenriNeural).
- Animation labiale **approximative** fondée sur l'amplitude audio, plus gestes de bras simples ; ce n'est pas une synchronisation phonétique et ce ne sont pas encore les portraits officiels.
- Workflow GitHub Actions manuel **« Pilote 3 questions - animation 2D (sans publication) »** dans `.github/workflows/pilot-3-questions.yml`.
- À exécuter dans GitHub Actions via **Run workflow** ; résultat attendu dans les artifacts `leo-prof-3-questions-pilote`. L'exécution et la qualité réelle du MP4 n'ont pas encore été vérifiées.
- **Aucune publication YouTube**, aucun déclencheur quotidien actif : obtenir l'accord sur le rendu avant d'automatiser la diffusion.
